from rest_framework import status, viewsets, serializers
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework import filters
from rest_framework.decorators import action
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from base.dynamic_filters.backends import DynamicDjangoFilterBackend
from base.frontend.utils import (
    build_candidate_admin_url,
    build_position_admin_url,
    build_agency_admin_url
)
from accounts.permissions import IsCompanyOrReadOnly
from accounts.models import User

from .serializers import (
    ProjectSerializer,
    PositionSerializer,
    PositionListSerializer,
    PositionCompanyListSerializer,
    ProjectCreateSetializer,
    PositionRetrieveSerializer,
    ShortPositionRetrieveSerializer,
    QuestionSerializer,
    PositionDocumentSerializer,
    ProjectDocumentSerializer,
)
from .models import (
    Project,
    Position,
    CandidatePositionApplication,
    AgencyPositionApplication,
    ProjectDocument,
    PositionDocument
)
from .permissions import (
    PositionProjectIsOwnerOrReadOnly,
    HasCompanyProfileOrReadOnly,
    HasCompanyProfile,
    HasCandidateProfile,
    HasCandidateOrAgencyProfile
)
from .filters import PositionFilter, PositionFilterStats


class PositionViewset(viewsets.ModelViewSet):
    """
    Position viewset [GET, POST, PUT, PATCH, DELETE]
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsCompanyOrReadOnly,
        PositionProjectIsOwnerOrReadOnly,
        HasCompanyProfileOrReadOnly
    )
    filter_class = PositionFilter
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DynamicDjangoFilterBackend
    )

    search_fields = ['position_title', 'position_title_de', 'position_title_en']
    ordering_fields = ['created', 'position_title']
    ordering = ['-created', '-modified']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(company=self.request.user.company_profile)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def get_serializer_class(self):
        listview_actions = ['list', 'metadata']
        detailview_actions = ['update', 'partial_update', 'create']
        if self.action in listview_actions:
            return PositionListSerializer
        if self.action in detailview_actions:
            return PositionSerializer
        if self.action == 'retrieve':
            if self.request.user.is_authenticated:
                return PositionRetrieveSerializer
            else:
                return ShortPositionRetrieveSerializer
        if self.action == 'apply':
            return serializers.Serializer
        if self.action == 'company_positions':
            return PositionCompanyListSerializer

        return super().get_serializer_class()

    def get_serializer_context(self):
        if self.action == 'retrieve' and self.request.user.is_authenticated:
            if self.request.user.user_type == User.USER_TYPE_CANDIDATE:
                return {
                    'candidate': self.request.user.candidate,
                    'request': self.request
                }
            elif self.request.user.user_type == User.USER_TYPE_AGENCY:
                return {
                    'agency': self.request.user.agency,
                    'request': self.request
                }
        return super().get_serializer_context()

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated, HasCompanyProfile])
    def company_positions(self, request):
        company = self.request.user.company_profile
        queryset = Position.objects.filter(company=company)
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True,
            permission_classes=[IsAuthenticated, HasCandidateOrAgencyProfile])
    def apply(self, request, *args, **kwargs):
        position = self.get_object()
        company_name = self.get_object().company.company_name
        contact_persons = self.get_object().company.get_contact_persons_email()
        position_url = build_position_admin_url(position.pk)
        if request.user.user_type == User.USER_TYPE_CANDIDATE:
            candidate_profile = request.user.candidate_profile
            full_name = candidate_profile.full_name
            candidate_url = build_candidate_admin_url(candidate_profile.pk)
            message = f"""New project position application\n
                          Candidate: {full_name} - {candidate_profile.user.email}\n{candidate_url}\n\n
                          Position: {company_name} - {contact_persons}\n{position_url}""",
            application, created = CandidatePositionApplication.objects.get_or_create(
                candidate=request.user.candidate_profile,
                position=position
            )
        elif request.user.user_type == User.USER_TYPE_AGENCY:
            agency_profile = request.user.agency_profile
            agency_name = agency_profile.company_name
            agency_contact_persons = agency_profile.get_contact_persons_email()
            agency_url = build_agency_admin_url(agency_profile.pk)
            message = f"""New project position application\n
                          Agency: {agency_name} - {agency_contact_persons}\n{agency_url}\n\n
                          Position: {company_name} - {contact_persons}\n{position_url}""",
            application, created = AgencyPositionApplication.objects.get_or_create(
                agency=request.user.agency_profile,
                position=position
            )

        if not created:
            return Response(
                {"detail": _('You have already applied for this position')},
                status=status.HTTP_400_BAD_REQUEST
            )
        send_mail(
            subject=_('Position application test'),
            message=message[0],
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.APPLY_POSITION_EMAIL],
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True,
            permission_classes=[IsAuthenticated, HasCandidateProfile],
            serializer_class=QuestionSerializer)
    def ask_question(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.data['question']
        candidate_profile = request.user.candidate_profile
        position_url = build_position_admin_url(self.get_object().pk)
        candidate_url = build_candidate_admin_url(candidate_profile.pk)
        full_name = candidate_profile.full_name
        company_name = self.get_object().company.company_name
        contact_persons = self.get_object().company.get_contact_persons_email()
        send_mail(
                subject=_('New candidate question'),
                message='New candidate question\n' +
                        f'From: {full_name} - {candidate_profile.user.email}\n{candidate_url}\n\n' +
                        f'To: {company_name} - {contact_persons}\n{position_url}\n\n' +
                        f'{question}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.ASK_QUESTION_EMAIL],
        )
        return Response(
            {"detail": _("Question has been successfully sent")},
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False,
            permission_classes=[IsAuthenticated, HasCompanyProfile],
            serializer_class=PositionDocumentSerializer)
    def upload_position_document(self, request):
        company = request.user.company_profile
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['company'] = company
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        company_name = company.company_name
        document_link = serializer.data.get('document')
        send_mail(
            subject=f'New position document was uploaded by {company_name}',
            message=f'New position document was uploaded by {company_name}\n' +
                    f'document: {document_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.COMPANY_PROJECTS_EMAIL],
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['get'], detail=False)
    def filters(self, request):
        data = DynamicDjangoFilterBackend(filterset_class=PositionFilterStats)\
            .get_dynamic_filters(self.request, self.get_queryset(), self)

        return Response(data)


class ProjectViewset(viewsets.ModelViewSet):
    """
    Project viewset [GET, POST, PUT, PATCH, DELETE]
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsCompanyOrReadOnly,
        PositionProjectIsOwnerOrReadOnly,
        HasCompanyProfileOrReadOnly
    )
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter
    )

    search_fields = ['project_name', 'project_name_de', 'project_name_en']
    ordering_fields = ['created', 'project_name']
    ordering = ['-created', '-modified']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(company=self.request.user.company_profile)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated, HasCompanyProfile])
    def company_projets(self, request):
        company = self.request.user.company_profile
        queryset = Project.objects.filter(company=company)
        queryset = self.filter_queryset(queryset)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False,
            permission_classes=[IsAuthenticated, HasCompanyProfile],
            serializer_class=ProjectDocumentSerializer)
    def upload_project_document(self, request):
        company = request.user.company_profile
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['company'] = company
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        company_name = company.company_name
        document_link = serializer.data.get('document')
        send_mail(
            subject=f'New project document was uploaded by {company_name}',
            message=f'New project document was uploaded by {company_name}\n' +
                    f'document: {document_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.COMPANY_PROJECTS_EMAIL],
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        retrieve_actions = ['retrieve', 'list', 'metadata']
        create_update_actions = ['create', 'update', 'partial_update']
        if self.action == 'upload_project_document':
            return ProjectDocumentSerializer
        if self.action in create_update_actions:
            return ProjectCreateSetializer
        if self.action in retrieve_actions:
            return ProjectSerializer


class ProjectDocumentViewset(viewsets.ModelViewSet):
    serializer_class = ProjectDocumentSerializer
    permission_classes = [IsAuthenticated, HasCompanyProfile]
    pagination_class = None

    def get_queryset(self):
        company = self.request.user.company_profile
        return ProjectDocument.objects.filter(company=company)

    def create(self, request, *args, **kwargs):
        company = request.user.company_profile
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['company'] = company
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        company_name = company.company_name
        document_link = serializer.data.get('document')
        send_mail(
            subject=f'New project document was uploaded by {company_name}',
            message=f'New project document was uploaded by {company_name}\n' +
                    f'document: {document_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.COMPANY_PROJECTS_EMAIL],
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PositionDocumentViewset(viewsets.ModelViewSet):
    serializer_class = PositionDocumentSerializer
    permission_classes = [IsAuthenticated, HasCompanyProfile]
    pagination_class = None

    def get_queryset(self):
        company = self.request.user.company_profile
        return PositionDocument.objects.filter(company=company)

    def create(self, request, *args, **kwargs):
        company = request.user.company_profile
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['company'] = company
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        company_name = company.company_name
        document_link = serializer.data.get('document')
        send_mail(
            subject=f'New position document was uploaded by {company_name}',
            message=f'New position document was uploaded by {company_name}\n' +
                    f'document: {document_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.COMPANY_PROJECTS_EMAIL],
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import IntegrityError
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework import filters, generics, serializers, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import Throttled
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from trench.serializers import UserMFAMethodSerializer
from trench.utils import user_token_generator
from trench.views.base import MFACodeLoginMixin, MFACredentialsLoginMixin

from base.dynamic_filters.backends import DynamicDjangoFilterBackend
from base.frontend.utils import (
    build_agency_admin_url,
    build_candidate_admin_url,
    build_candidate_cv_url,
    build_company_admin_url,
)
from base.utils import build_frontend_url
from projects.permissions import HasCompanyProfile
from projects.serializers import QuestionSerializer

from .filters import AgencyFilter, AgencyFilterStats, CandidateFilter, CandidateFilterStats
from .models import (
    AgencyCandidateCV,
    AgencyHiring,
    AgencyProfile,
    CandidateCV,
    CandidateHiring,
    CandidateProfile,
    CompanyProfile,
    EmployeeProfile,
    Specialization,
    Technology,
    User,
)
from .permissions import (
    IsAgency,
    IsAgencyOrReadOnly,
    IsCandidateOrReadOnly,
    IsCompanyOrAgency,
    IsCompanyOrReadOnly,
    IsEmployeeOrReadOnly,
    IsOwnerOrReadOnly,
)
from .serializers import (
    AccountInfoRetrieveSerializer,
    AgencyCVSerializer,
    AgencyProfileListSerializer,
    AgencyProfileSerializer,
    CandidateProfileSerializer,
    ChangePasswordSerializer,
    CheckEmailSerializer,
    CompanyProfileSerializer,
    CVSerializer,
    DeleteAccountSerializer,
    EmployeeProfileSeializer,
    JWTAuthSerializer,
    RegisterUserSerializer,
    ShortAgencyProfileSerializer,
    ShortCandidateProfileSerializer,
    ShortCompanyProfileSerializer,
    SpecializationSerializer,
    TechnologySerializer,
    UploadCompanyDocumentSerializer,
)
from .tokens import change_email_token, user_activation_token


class CreateUserAPIView(generics.CreateAPIView):
    """
    Creates and saves a User with the given email and password.
    """
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user_type = serializer.validated_data.get('user_type')
        user_obj = User(email=email, user_type=user_type)
        user_obj.set_password(password)
        user_obj.save()
        current_site = get_current_site(self.request)
        prefix = '/api/v1/accounts/activate/'
        uid = urlsafe_base64_encode(force_bytes(user_obj.pk))
        token = user_activation_token.make_token(user_obj)

        confirmation_url = settings.TRANSFER_PROTOCOL + current_site.domain + prefix + uid + '/' + token + '/'
        html_message = loader.render_to_string(
            'accounts/activation_letter.html',
            {'confirmation_url': confirmation_url}
        )
        send_mail(
            subject=_('Confirm Your Email Address'),
            message=_('Please confirm your email address'),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_obj.email],
            html_message=html_message
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ActivateView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            user = None
        if user and user_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect(build_frontend_url('login'))
        else:
            if user and user.is_active:
                return redirect(build_frontend_url('login'))
            else:
                msg = _('Activation link is invalid!')
                return HttpResponse(msg, status=404)


class IdentificateCandidateProfileView(views.APIView):
    """
    Endpoint creates request to a support team for manual user identification
    """
    serializer_class = serializers.Serializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            candidate = request.user.candidate_profile
            candidate_url = build_candidate_admin_url(candidate.pk)
            message = f'New candidate for identification\n' \
                      f'Candidate: {candidate.full_name} (profile id {candidate.pk}) - {candidate.email}\n' \
                      f'{candidate_url}'
            if candidate.is_identified:
                return Response(
                    {"detail": _('This profile is already identified')},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ObjectDoesNotExist:
            candidate = request.user
            if candidate.candidate_cvs.exists():
                document = candidate.candidate_cvs.last()
                document_url = build_candidate_cv_url(document.pk)
            else:
                document_url = None
            message = f'New candidate for identification\n' \
                      f'Candidate: {candidate.email}\n' \
                      f'Document: {document_url}'
        finally:
            send_mail(
                subject='Candidate identification',
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.IDENTIFICATE_CANDIDATE_EMAIL],
            )
            return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user

        return obj

    def get_serializer_context(self):
        return {
            'user': self.get_object()
        }

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        # If user has password
        # Social auth performing registration without password
        has_password = user.has_password

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check old password if exists
        if not user.check_password(
                serializer.data.get("old_password")
        ) and has_password:
            return Response(
                {"old_password": [_("Incorrect password")]},
                status=status.HTTP_400_BAD_REQUEST
            )
        # set_password also hashes the password that the user will get
        user.set_password(serializer.data.get("new_password"))
        user.save()
        response = {
            'detail': _('Password updated successfully'),
        }
        html_message = loader.render_to_string(
            'accounts/change_password_letter.html',
        )
        send_mail(
            subject=_('Password Change'),
            message=_('Your password has been changed'),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message
        )

        return Response(response, status=status.HTTP_200_OK)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token,
                                 *args, **kwargs):
    html_message = loader.render_to_string(
        'accounts/password_reset_letter.html',
        {'reset_code': reset_password_token.key}
    )
    send_mail(
        subject=_('Reset password'),
        message=_('Reset password'),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[reset_password_token.user.email],
        html_message=html_message
    )


class CheckEmailView(generics.GenericAPIView):
    """
    An endpoint for changing account email.
    """
    serializer_class = CheckEmailSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_obj = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_email = serializer.validated_data.get('email')
        current_site = get_current_site(self.request)
        prefix = '/api/v1/accounts/change_email/'
        uid = urlsafe_base64_encode(force_bytes(user_obj.pk)),
        token = change_email_token.make_token(user_obj),
        change_email_url = f'{settings.TRANSFER_PROTOCOL}' \
            + f'{current_site.domain}{prefix}{uid[0]}/' \
            + f'{token[0]}/{new_email}/'
        html_message = loader.render_to_string(
            'accounts/change_email_letter.html',
            {
                'change_email_url': change_email_url,
                'new_email': new_email
            }
        )
        send_mail(
            subject=_('Email Change Confirmation Letter'),
            message=_('Please confirm your email changing'),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_obj.email],
            html_message=html_message
        )
        return Response(
            {"detail": f"Email Change Confirmation Letter was sent to {user_obj.email}"},
            status=status.HTTP_200_OK
        )


class ChangeEmailView(views.APIView):
    """
    An endpoint for changing email confirmation.
    """

    def get(self, request, uidb64, token, email):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            email = email
        except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            user = None
        if user is not None and change_email_token.check_token(user, token):
            user.email = email
            user.save()
            return redirect(build_frontend_url('login'))
        else:
            msg = _('Change email link is invalid!')
            return HttpResponse(msg, status=404)


class DeleteAccountView(generics.DestroyAPIView):
    """
    An endpoint for deleting account by DELETE method.
    """
    serializer_class = DeleteAccountSerializer
    permission_classes = (IsAuthenticated,
                          IsCandidateOrReadOnly)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if instance.check_password(serializer.data.get("password")):
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"password": [_("Incorrect password")]},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"password": [_("This field may not be blank.")]},
            status=status.HTTP_400_BAD_REQUEST)


class UploadCVView(generics.CreateAPIView):
    """
    Endpoint for candidates to upload CV
    """
    serializer_class = CVSerializer
    permission_classes = (IsAuthenticated, IsCandidateOrReadOnly)
    throttle_scope = 'uploads'

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        protocol = settings.TRANSFER_PROTOCOL
        current_site = get_current_site(request)
        user_link = f'{protocol}{current_site}/admin/accounts/user/{user.id}/change/'
        cv_link = serializer.data.get('cv_file')
        send_mail(
            subject=f'New CV was uploaded by {user.email}',
            message=f'New CV was uploaded by {user.email} \nuser: {user_link} \nCV: {cv_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.CANDIDATE_PROFILE_EMAIL],
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def throttled(self, request, wait):
        raise Throttled(detail={
            "detail": _("You can't upload more than 3 CVs per 24 hours."),
            "available_in": f"{wait} seconds"
        })


class CVViewset(viewsets.ModelViewSet):
    serializer_class = CVSerializer
    permission_classes = (IsAuthenticated, IsCandidateOrReadOnly)
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return CandidateCV.objects.filter(user=user)

    def get_throttles(self):
        if self.request.method.lower() == 'post':
            self.throttle_scope = 'uploads'
        return super(CVViewset, self).get_throttles()

    def throttled(self, request, wait):
        raise Throttled(detail={
            "detail": _("You can't upload more than 3 CVs per 24 hours."),
            "available_in": f"{wait} seconds"
        })

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        protocol = settings.TRANSFER_PROTOCOL
        current_site = get_current_site(request)
        user_link = f'{protocol}{current_site}/admin/accounts/user/{user.id}/change/'
        cv_link = serializer.data.get('cv_file')
        send_mail(
            subject=f'New CV was uploaded by {user.email}',
            message=f'New CV was uploaded by {user.email} \nuser: {user_link} \nCV: {cv_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.CANDIDATE_PROFILE_EMAIL],
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AgencyCandidateCVViewset(viewsets.ModelViewSet):
    serializer_class = AgencyCVSerializer
    permission_classes = (IsAuthenticated, IsAgency)
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return AgencyCandidateCV.objects.filter(user=user)


class UploadCompanyDocumentView(generics.CreateAPIView):
    """
    Endpoint for companies and agencies to upload documents
    """
    serializer_class = UploadCompanyDocumentSerializer
    permission_classes = (IsAuthenticated, IsCompanyOrAgency)
    throttle_scope = 'uploads'

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        protocol = settings.TRANSFER_PROTOCOL
        current_site = get_current_site(request)
        user_link = f'{protocol}{current_site}/admin/accounts/user/{user.id}/change/'
        document_link = serializer.data.get('document')
        if user.user_type == User.USER_TYPE_COMPANY:
            recipient_list = [settings.COMPANY_PROFILE_EMAIL]
        elif user.user_type == User.USER_TYPE_AGENCY:
            recipient_list = [settings.AGENCY_PROFILE_EMAIL]
        send_mail(
            subject=f'New document was uploaded by {user.email}',
            message=f'New document was uploaded by {user.email} \nuser: {user_link} \ndocument: {document_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def throttled(self, request, wait):
        raise Throttled(detail={
            "detail": _("You can't upload more than 3 documents per 24 hours."),
            "available_in": f"{wait} seconds"
        })


class CandidateProfileVieswSet(viewsets.ModelViewSet):
    """
    Candidate profile viewset [GET, POST, PUT, PATCH, DELETE]
    ---
    communication_languages -- [string] (Alpha 2 codes of languages)
    job_type -- [int] (1-Full time, 2-Part time, 3-Contract, 4-Internship)
    additional_links -- [obj] (Nested objects with string field "url")
    first_name -- string
    last_name -- string
    image -- string
    job_position -- string
    cover_letter -- string
    date_of_birth -- string
    experience -- int (1- <1 year, 2- 1…3 years, 3- 3…5 years, 4- 5+ years)
    experience_level -- int (1-Junior, 2-Middle, 3-Senior, 4-Lead)
    phone_number -- string
    email -- string
    linkedin_url -- string
    technologies -- [int] (Technologies id)
    """

    queryset = CandidateProfile.objects.all()
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
        IsCandidateOrReadOnly
    )
    filter_class = CandidateFilter
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DynamicDjangoFilterBackend,
    )

    search_fields = ['job_position', 'job_position_de', 'job_position_en']
    ordering_fields = ['created', 'job_position']
    ordering = ['-created', '-modified']

    def get_serializer_class(self):
        retrieve_actions = ['list', 'metadata', 'retrieve']
        if self.action in retrieve_actions:
            return ShortCandidateProfileSerializer
        if self.action == 'hire':
            return serializers.Serializer
        if self.action == 'ask_question':
            return QuestionSerializer
        return CandidateProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(user=self.request.user)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except IntegrityError:
            return Response(
                {"detail": _("This user already has profile")},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['post'], detail=True,
            permission_classes=[IsAuthenticated, HasCompanyProfile])
    def hire(self, request, *args, **kwargs):
        candidate = self.get_object()
        company = request.user.company_profile
        company_profile = request.user.company_profile
        company_url = build_company_admin_url(company.pk)
        candidate_url = build_candidate_admin_url(candidate.pk)
        contact_persons = company_profile.get_contact_persons_email()
        hiring, created = CandidateHiring.objects.get_or_create(
            company=company,
            candidate=candidate
        )
        if not created:
            return Response(
                {"detail": _('You have already hired this candidate')},
                status=status.HTTP_400_BAD_REQUEST
            )
        send_mail(
            subject='Candidate hiring',
            message='New candidate hiring\n' +
                    f'Company: {company.company_name} - {contact_persons}\n{company_url}\n\n' +
                    f'Candidate: {candidate.full_name} - {candidate.email}\n{candidate_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.HIRE_CANDIDATE_EMAIL],
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True,
            permission_classes=[IsAuthenticated, HasCompanyProfile])
    def ask_question(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.data['question']
        candidate_profile = self.get_object()
        company_profile = request.user.company_profile
        company_url = build_company_admin_url(company_profile.pk)
        candidate_url = build_candidate_admin_url(candidate_profile.pk)
        full_name = candidate_profile.full_name
        company_name = company_profile.company_name
        contact_persons = company_profile.get_contact_persons_email()
        send_mail(
                subject='New company question',
                message='New company question\n' +
                        f'From: {company_name} - {contact_persons}\n{company_url}\n\n' +
                        f'To: {full_name} - {candidate_profile.email}\n{candidate_url}\n\n' +
                        f'{question}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.ASK_QUESTION_EMAIL],
        )
        return Response(
            {"detail": _("Question has been successfully sent")},
            status=status.HTTP_200_OK
        )

    @action(methods=['get'], detail=False)
    def filters(self, request):
        data = DynamicDjangoFilterBackend(filterset_class=CandidateFilterStats)\
            .get_dynamic_filters(self.request, self.get_queryset(), self)

        return Response(data)


class CompanyProfileVieswSet(viewsets.ModelViewSet):
    """
    Company profile viewset [GET, POST, PUT, PATCH, DELETE]
    ---
    communication_languages -- [string] (Alpha 2 codes of languages)
    additional_links -- [obj] (Nested objects with string field "url")
    contact_persons -- [obj] (Nested object with string fields:
        "first_name",
        "last_name",
        "phone_number",
        "email")
    company_logo -- string
    company_name -- string
    company_adress -- string
    company_description -- string
    company_size -- int (1-'<50', 2-'50-200', 3-'200-500', 4-'500+')
    industry -- string
    company_website -- string
    """

    queryset = CompanyProfile.objects.all()
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
        IsCompanyOrReadOnly
    )
    filter_backends = [filters.OrderingFilter, ]
    ordering_fields = ['created', 'company_name']
    ordering = ['-created', '-modified']

    def get_serializer_class(self):
        retrieve_actions = ['list', 'metadata', 'retrieve']
        if self.action in retrieve_actions:
            return ShortCompanyProfileSerializer
        return CompanyProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(user=self.request.user)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except IntegrityError:
            return Response(
                {"detail": _("This user already has profile")},
                status=status.HTTP_400_BAD_REQUEST
            )


class AgencyProfileVieswSet(viewsets.ModelViewSet):
    """
    Agency profile viewset [GET, POST, PUT, PATCH, DELETE]
    ---
    communication_languages -- [string] (Alpha 2 codes of languages)
    additional_links -- [obj] (Nested objects with string field "url")
    contact_persons -- [obj] (Nested object with string fields:
        "first_name",
        "last_name",
        "phone_number",
        "email")
    company_logo -- string
    company_name -- string
    company_adress -- string
    company_description -- string
    number_of_specialists -- int (1-'<5', 2-'5-10', 3-'10-20', 4-'>20')
    company_website -- string
    """

    queryset = AgencyProfile.objects.all()
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
        IsAgencyOrReadOnly
    )
    filter_class = AgencyFilter
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DynamicDjangoFilterBackend,
    ]
    ordering_fields = ['created', 'company_name']
    ordering = ['-created', '-modified']

    def get_serializer_class(self):
        retrieve_actions = ['metadata', 'retrieve']
        if self.action == 'list':
            return AgencyProfileListSerializer
        if self.action in retrieve_actions:
            return ShortAgencyProfileSerializer
        elif self.action == 'ask_question':
            return QuestionSerializer
        elif self.action == 'hire':
            return serializers.Serializer
        return AgencyProfileSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        if self.action in ('retrieve', 'update', 'partial_update', 'destroy') \
                and self.request.user and self.request.user.agency:
            return qs.filter_active_or_owner(self.request.user.agency)

        return qs.filter_active()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(user=self.request.user)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except IntegrityError:
            return Response(
                {"detail": _("This user already has profile")},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['post'], detail=True,
            permission_classes=[IsAuthenticated, HasCompanyProfile])
    def ask_question(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.data['question']
        agency_profile = self.get_object()
        company_profile = request.user.company_profile
        company_url = build_company_admin_url(company_profile.pk)
        agency_url = build_agency_admin_url(agency_profile.pk)
        agency_name = agency_profile.company_name
        company_name = company_profile.company_name
        contact_persons = company_profile.get_contact_persons_email()
        agency_contact_persons = agency_profile.get_contact_persons_email()
        send_mail(
                subject='New company question',
                message='New company question\n' +
                        f'From: {company_name} - {contact_persons}\n{company_url}\n\n' +
                        f'To: {agency_name} - {agency_contact_persons}\n{agency_url}\n\n' +
                        f'{question}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.ASK_QUESTION_EMAIL],
        )
        return Response(
            {"detail": _("Question has been successfully sent")},
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=True,
            permission_classes=[IsAuthenticated, HasCompanyProfile])
    def hire(self, request, *args, **kwargs):
        agency = self.get_object()
        company = request.user.company_profile
        company_profile = request.user.company_profile
        company_url = build_company_admin_url(company.pk)
        agency_url = build_agency_admin_url(agency.pk)
        contact_persons = company_profile.get_contact_persons_email()
        agency_contact_persons = agency.get_contact_persons_email()
        hiring, created = AgencyHiring.objects.get_or_create(
            company=company,
            agency=agency
        )
        if not created:
            return Response(
                {"detail": _('You have already hired this agency')},
                status=status.HTTP_400_BAD_REQUEST
            )
        send_mail(
            subject='Agency hiring',
            message='New agency hiring\n' +
                    f'Company: {company.company_name} - {contact_persons}\n{company_url}\n\n' +
                    f'Agency: {agency.company_name} - {agency_contact_persons}\n{agency_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.HIRE_CANDIDATE_EMAIL],
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def filters(self, request):
        data = DynamicDjangoFilterBackend(filterset_class=AgencyFilterStats)\
            .get_dynamic_filters(self.request, self.get_queryset(), self)

        return Response(data)


class EmployeeProfileViewset(viewsets.ModelViewSet):
    """
    Employee viewset
    """
    serializer_class = EmployeeProfileSeializer
    permission_classes = (IsAuthenticated, IsEmployeeOrReadOnly)

    def get_queryset(self):
        user = self.request.user
        if user.user_type == User.USER_TYPE_AGENCY or user.user_type == User.USER_TYPE_COMPANY:
            return EmployeeProfile.objects.filter(user__employer=user)
        elif user.user_type == User.USER_TYPE_EMPLOYEE:
            return EmployeeProfile.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(user=self.request.user)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except IntegrityError:
            return Response(
                {"detail": _("This user already has profile")},
                status=status.HTTP_400_BAD_REQUEST
            )


class TechnologyViewset(viewsets.ReadOnlyModelViewSet):
    """
    Technologies list and detail viewset
    """
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class SpecializationViewset(viewsets.ReadOnlyModelViewSet):
    """
    Specializations list and detail viewset
    """
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class ObtainJSONWebTokenMixin:
    def handle_user_login(self, request, serializer, *args, **kwargs):
        return Response(JWTAuthSerializer(serializer.user).data)


class ExtendedMFACredentialsLoginMixin(MFACredentialsLoginMixin):

    def handle_mfa_response(self, user, mfa_method, *args, **kwargs):
        data = {
            'ephemeral_token': user_token_generator.make_token(user),
            'method': mfa_method.name,
            'other_methods': UserMFAMethodSerializer(
                user.mfa_methods.filter(is_active=True, is_primary=False),
                many=True,
            ).data,
        }
        if mfa_method.name == 'sms':
            data['censored_phone_number'] = user.censored_phone_number
        return Response(data)


class CustomJSONWebTokenLoginOrRequestMFACode(ExtendedMFACredentialsLoginMixin,
                                              ObtainJSONWebTokenMixin,
                                              generics.GenericAPIView):
    pass


class CustomJSONWebTokenLoginWithMFACode(MFACodeLoginMixin,
                                         ObtainJSONWebTokenMixin,
                                         generics.GenericAPIView):
    pass


class AccountInfoAPiView(generics.GenericAPIView):
    """
    Endpoint shows self account information
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(AccountInfoRetrieveSerializer(self.request.user).data)

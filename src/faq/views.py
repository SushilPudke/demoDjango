from django.core.mail import send_mail
from django.conf import settings

from rest_framework import generics, filters, status
from rest_framework.response import Response
from django_filters import rest_framework as dj_filters
from rest_framework.permissions import AllowAny

from .models import Question
from .serializers import QuestionSerializer, ContactFormSerializer


class QuestionListView(generics.ListAPIView):
    """
    Endpoint returns list of FAQ
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter, dj_filters.DjangoFilterBackend)
    search_fields = ['question_headline', 'answer']
    filterset_fields = ['question_type']
    pagination_class = None


class ContactFormApiView(generics.GenericAPIView):
    """
    Endpoint for contact with support
    """
    serializer_class = ContactFormSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        full_name = serializer.data['full_name']
        email = serializer.data['email']
        question = serializer.data['question']
        send_mail(
            subject=f'New question or request from {email}',
            message=f'Email: {email} \nFull name: {full_name} \nQuestion of request: {question}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.SUPPORT_EMAIL],
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

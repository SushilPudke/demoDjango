from rest_framework import serializers, views
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from django.conf import settings


class TranslationSettingsView(views.APIView):
    """
    Endpoint returns for translation settigs for FE
    only for admin users
    """
    serializer_class = serializers.Serializer
    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        return Response({
            "REACT_APP_USERNAME": settings.REACT_APP_USERNAME,
            "REACT_APP_REPO_OWNER": settings.REACT_APP_REPO_OWNER,
            "REACT_APP_REPO_NAME": settings.REACT_APP_REPO_NAME,
            "REACT_APP_REPO_BRANCH": settings.REACT_APP_REPO_BRANCH,
            "REACT_APP_TOKEN": settings.REACT_APP_TOKEN
        })

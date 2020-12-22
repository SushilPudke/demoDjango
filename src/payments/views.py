from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from accounts.permissions import IsAgency
from payments.serializers import AgencySubscriptionSerializer


class AgencySubscriptionView(mixins.CreateModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = AgencySubscriptionSerializer
    permission_classes = (IsAgency, )

    def create(self, request, *args, **kwargs):
        return Response(
            self.get_serializer(instance=request.user).data,
            status=status.HTTP_200_OK
        )

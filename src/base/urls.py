from rest_framework import routers

from base.views import (
    ConstantsViewSet
)


router = routers.DefaultRouter()

router.register('constants', ConstantsViewSet, basename='constants')

urlpatterns = router.urls

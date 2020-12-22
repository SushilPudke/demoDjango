from rest_framework import routers

from sitemap.views import (
    SitemapViewSet
)


router = routers.DefaultRouter()

router.register('sitemap.xml', SitemapViewSet, basename='sitemap')

urlpatterns = router.urls

from rest_framework import viewsets
from django.http import HttpResponse

from sitemap.utils import SITEMAP_PATH


class SitemapViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        return HttpResponse(open(SITEMAP_PATH).read(), content_type='text/xml; charset=utf-8')

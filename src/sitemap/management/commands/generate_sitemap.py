from django.core.management.base import BaseCommand

from sitemap.tasks import build_sitemap_xml


class Command(BaseCommand):
    help = 'Generate sitemap'

    def handle(self, *args, **options):
        build_sitemap_xml()

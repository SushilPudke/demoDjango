from xml.dom import minidom

from celeryapp import app

from accounts.models import CandidateProfile
from projects.models import Position
from sitemap.utils import (
    generate_xhtml_sitemap_body,
    generate_xhtml_localized_url_blocks,
    SITEMAP_PATH,
)


SITEMAP_DEFAULTS = [
    '',
    'jobs',
    'candidates',
    'aboutus',
    'faqs',
]


def build_candidates() -> list:
    return [
        f'candidate/{pk}' for pk in
        CandidateProfile.objects.values_list('pk', flat=True)
    ]


def build_jobs() -> list:
    return [
        f'position/{pk}' for pk in
        Position.objects.values_list('pk', flat=True)
    ]


SITEMAP_URL_BACKENDS = [
    build_candidates,
    build_jobs
]


def build_sitemap():
    all_links = SITEMAP_DEFAULTS

    for backend in SITEMAP_URL_BACKENDS:
        all_links += backend()

    return generate_xhtml_sitemap_body([
        generate_xhtml_localized_url_blocks(link)
        for link in all_links
    ])


def build_sitemap_xml():
    xml_str = minidom.parseString(build_sitemap()).toprettyxml(indent="   ")

    with open(SITEMAP_PATH, 'w') as f:
        f.write(xml_str)


@app.task
def generate_sitemap_task():
    build_sitemap_xml()

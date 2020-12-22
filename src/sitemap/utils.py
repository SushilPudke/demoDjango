import os.path

from base.languages.constants import COUNTRY_EN, COUNTRY_DE
from base.frontend.utils import build_frontend_url
from django.conf import settings

SITEMAP_LANGUAGES = (
    COUNTRY_EN,
    COUNTRY_DE,
)

SITEMAP_MEDIA_DIR = os.path.join(settings.BASE_DIR, 'sitemap', 'media')
SITEMAP_PATH = os.path.join(SITEMAP_MEDIA_DIR, 'sitemap.xml')


def generate_localized_link(link: str, lang=COUNTRY_EN):
    lang = lang if lang != COUNTRY_EN else ''

    return build_frontend_url(os.path.join(lang, link))


def generate_xhtml_link(href, **args):
    defaults = {
        'rel': 'alternate',
        'href': href
    }

    defaults.update(args)

    return '<xhtml:link {} />'.format(
        ' '.join([f'{tag}="{value}"' for tag, value in defaults.items()])
    )


def generate_localized_xhtml_link(href, hreflang=COUNTRY_EN, **kwargs):
    kwargs.update({'hreflang': hreflang})

    return generate_xhtml_link(href, **kwargs)


def generate_xhtml_url_block(url, initial_lang=COUNTRY_EN):
    links = [generate_localized_xhtml_link(
        generate_localized_link(url, lang=lang), hreflang=lang
    ) for lang in SITEMAP_LANGUAGES]

    return '<url><loc>{}</loc>{}</url>'.format(generate_localized_link(url, lang=initial_lang), "".join(links))


def generate_xhtml_localized_url_blocks(url):
    return ''.join(
        [
            generate_xhtml_url_block(url, initial_lang=lang)
            for lang in SITEMAP_LANGUAGES
        ]
    )


def generate_xhtml_sitemap_body(body: list):
    return """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="https://www.w3.org/1999/xhtml">{}
    </urlset>""".format(''.join(body))

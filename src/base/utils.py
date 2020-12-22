import os.path
from json import dumps
from urllib.parse import (
    urlencode,
    unquote,
    urlparse,
    parse_qsl,
    ParseResult,
    urljoin
)

from django.conf import settings
from django.templatetags.static import static


def build_frontend_url(path):
    return urljoin(settings.FRONTEND_URL, path.lstrip('/'))


def build_backend_url(path):
    return urljoin(settings.BACKEND_URL, path.lstrip('/'))


def absolute_static_path(path):
    return os.path.join(settings.BACKEND_URL, static(path).strip('/'))


def add_url_params(url, params):
    """ Add GET params to provided URL being aware of existing.
    :param url: string of target URL
    :param params: dict containing requested params to be added
    :return: string with updated URL
    """
    url = unquote(url)
    parsed_url = urlparse(url)
    get_args = parsed_url.query
    parsed_get_args = dict(parse_qsl(get_args))
    parsed_get_args.update(params)

    parsed_get_args.update(
        {k: dumps(v) for k, v in parsed_get_args.items()
         if isinstance(v, (bool, dict))}
    )

    encoded_get_args = urlencode(parsed_get_args, doseq=True)
    new_url = ParseResult(
        parsed_url.scheme, parsed_url.netloc, parsed_url.path,
        parsed_url.params, encoded_get_args, parsed_url.fragment
    ).geturl()

    return new_url

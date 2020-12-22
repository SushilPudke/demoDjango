from __future__ import absolute_import, unicode_literals

from .common import *  # noqa
from .common import REDIS_URL, REDIS_MAX_CONNECTIONS


CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        'OPTIONS': {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                # Hobby redistogo on heroku only supports max. 10, increase as required.
                'max_connections': REDIS_MAX_CONNECTIONS,
                'timeout': 20,
            }
        }
    }
}

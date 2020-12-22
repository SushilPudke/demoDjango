from __future__ import absolute_import, unicode_literals
import logging

from .common import *  # noqa

MEDIA_ROOT = "/tmp"

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

NOSE_ARGS = [
    '--nologcapture',
    '--nocapture',
]

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

logging.disable(logging.CRITICAL)

FILE_UPLOAD_HANDLERS = ["django.core.files.uploadhandler.MemoryFileUploadHandler", ]

# Enable to see slow test benchmark
# It is disabled by default because it skips some tests
# TEST_RUNNER = 'django_slowtests.testrunner.DiscoverSlowestTestsRunner'
NUM_SLOW_TESTS = 100

# (Optional)
SLOW_TEST_THRESHOLD_MS = 200  # Only show tests slower than 200ms

# (Optional)
ALWAYS_GENERATE_SLOW_REPORT = True  # Generate report only when requested using --slowreport flag

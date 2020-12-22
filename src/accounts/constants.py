from django.utils.translation import ugettext_lazy as _

LANGUAGES = [
    ('en', _('English')),
    ('de', _('German'))
]

EXPERIENCE = (
    (1, _('< 1 year')),
    (2, _('1-3 years')),
    (3, _('3-5 years')),
    (4, _('5+ years'))
)

EXPERIENCE_LVL = (
    (1, _('Junior')),
    (2, _('Middle')),
    (3, _('Senior')),
    (4, _('Lead'))
)

JOB_TYPE = (
    (1, _('Full time')),
    (2, _('Part time')),
    (3, _('Contract')),
    (4, _('Internship'))
)

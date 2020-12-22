from rest_framework import viewsets
from rest_framework.response import Response

from accounts.models import Specialization, Technology
from accounts.serializers import SpecializationSerializer, TechnologySerializer
from accounts.constants import EXPERIENCE, EXPERIENCE_LVL, JOB_TYPE, LANGUAGES
from projects.constants import CURRENCIES
from base.languages.constants import COUNTRY_CHOICES, COUNTRY_AVAILABLE_CHOICES


def convert_choices(const):
    return [
        {'value': x[0], 'label': x[1]}
        for x in const
    ]


class ConstantsViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        return Response({
            'specialization': SpecializationSerializer(Specialization.objects.all(), many=True).data,
            'technology': TechnologySerializer(Technology.objects.all(), many=True).data,
            'experience': convert_choices(EXPERIENCE),
            'experience_level': convert_choices(EXPERIENCE_LVL),
            'job_type': convert_choices(JOB_TYPE),
            'communication_languages': convert_choices(LANGUAGES),
            'country': convert_choices(COUNTRY_CHOICES),
            'position_country': convert_choices(COUNTRY_AVAILABLE_CHOICES),
            'currency': [
                {'value': x[0], 'label': x[0]}
                for x in CURRENCIES
            ]
        })

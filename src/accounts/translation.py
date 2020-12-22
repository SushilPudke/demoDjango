from modeltranslation.translator import register, TranslationOptions
from .models import CompanyProfile, CandidateProfile, AgencyProfile


@register(CompanyProfile)
class CompanyProfileTranslationOptions(TranslationOptions):
    fields = (
        'company_name',
        'company_adress',
        'city',
        'company_description',
        'industry'
    )


@register(AgencyProfile)
class AgencyProfileTranslationOptions(TranslationOptions):
    fields = (
        'company_name',
        'company_adress',
        'city',
        'company_description'
    )


@register(CandidateProfile)
class CandidateProfileTranslationOptions(TranslationOptions):
    fields = (
        'nationality',
        'job_position',
        'cover_letter',
        'adress',
        'city',
    )

import os

import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.core.exceptions import ObjectDoesNotExist
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from drf_writable_nested.serializers import NestedCreateMixin, NestedUpdateMixin
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from base.utils import build_backend_url
from authentication.social.linkedin import LinkedinOAuth2
from .constants import JOB_TYPE
from .models import (
    LANGUAGES,
    AgencyCandidateCV,
    AgencyContactPerson,
    AgencyLink,
    AgencyProfile,
    AverageHourlyRate,
    CandidateCV,
    CandidateLink,
    CandidateProfile,
    CompanyDocument,
    CompanyProfile,
    ContactPerson,
    EmployeeProfile,
    HourlyRate,
    Link,
    MonthlyRate,
    Specialization,
    Technology,
    User,
)
from .validators import (
    AgeRestrictionValidator,
    FileSizeValidator,
    FutureDateValidator,
    ImageSizeValidator,
    LinkedinUrlValidator,
    PnoneNumberValidator,
    UppercaseValidator,
)


class UserSerializer(serializers.ModelSerializer):
    sms_phone_number = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'user_type',
            'sms_phone_number',
            'has_password',
            'membership_active',
            'membership_activated_date',
        ]

    def get_sms_phone_number(self, obj):
        return obj.censored_phone_number


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'user_type'
        )
        extra_kwargs = {
            'password': {
                'required': True,
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            'user_type': {
                'allow_null': False,
                'required': True
            }
        }

    def validate_email(self, value):
        norm_email = value.lower()
        if User.objects.filter(email=norm_email).exists():
            raise serializers.ValidationError(
                _("This email has been already registered in our system.")
            )
        return norm_email

    def validate(self, data):
        password = data.get('password')
        errors = dict()
        try:
            validators.validate_password(password=password)
            UppercaseValidator.validate(self, password=password)

        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(RegisterUserSerializer, self).validate(data)


class UserProfileRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', )

    @property
    def profile_type_mapping(self):
        return {
            User.USER_TYPE_CANDIDATE: CandidateProfileRetrieveSerializer,
            User.USER_TYPE_COMPANY: CompanyProfileRetrieveSerializer,
            User.USER_TYPE_AGENCY: AgencyProfileRetrieveSerializer,
            User.USER_TYPE_EMPLOYEE: EmployeeProfileSeializer
        }

    def to_representation(self, instance):
        serializer = self.profile_type_mapping[instance.user_type]

        return serializer(instance.profile).data if instance.profile else {}


class AccountInfoRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()
    profile_prefill = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'user',
            'profile',
            'profile_prefill',
        )

    def get_user(self, obj):
        return UserSerializer(self.instance, read_only=True).data

    def get_profile(self, obj):
        return UserProfileRetrieveSerializer(self.instance).data or None

    def get_profile_prefill(self, obj):
        social = self.instance.social_auth.filter(provider=LinkedinOAuth2.name).first()

        if not social:
            return {}

        return LinkedinOAuth2.profile_extractor(social).extract_data()


class JWTAuthSerializer(AccountInfoRetrieveSerializer):
    refresh = serializers.SerializerMethodField()
    access = serializers.SerializerMethodField()

    class Meta(AccountInfoRetrieveSerializer.Meta):
        fields = AccountInfoRetrieveSerializer.Meta.fields + (
            'refresh',
            'access',
        )

    @cached_property
    def token(self):
        return RefreshToken.for_user(self.instance)

    def get_refresh(self, obj):
        return str(self.token)

    def get_access(self, obj):
        return str(self.token.access_token)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=False,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )

    @property
    def user(self):
        return self.context.get('user')

    def validate(self, data):
        # Checking user has a password and it is valid
        if self.user.has_password and not data.get('old_password'):
            raise serializers.ValidationError(_('Password is required field'))

        password = data.get('new_password')
        errors = dict()
        try:
            validators.validate_password(password=password)
            UppercaseValidator.validate(self, password=password)
        except exceptions.ValidationError as e:
            errors['new_password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(ChangePasswordSerializer, self).validate(data)


class CVSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    document_name = serializers.SerializerMethodField('get_filename')

    class Meta:
        model = CandidateCV
        fields = ['cv_file', 'document_name', 'user']

    def validate_cv_file(self, value):
        FileSizeValidator.validate(self, file=value)
        return value

    def get_filename(self, value):
        try:
            url = value.cv_file.url
        except (AttributeError, ValueError):
            return None
        return os.path.basename(url)


class AgencyCVSerializer(CVSerializer):

    class Meta:
        model = AgencyCandidateCV
        fields = ['id', 'cv_file', 'document_name', 'user']


class UploadCompanyDocumentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CompanyDocument
        fields = '__all__'

    def validate_document(self, value):
        FileSizeValidator.validate(self, file=value)
        return value


class CandidateLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateLink
        fields = ('url',)
        extra_kwargs = {
            "url": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}}
        }


class AgencyLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencyLink
        fields = ('url',)
        extra_kwargs = {
            "url": {"error_messages": {
                "max_length": _("Please enter maximum 255 symbols"),
                "invalid": _("Invalid URL address")
            }}
        }


class CompanyLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('url',)
        extra_kwargs = {
            "url": {"error_messages": {
                "max_length": _("Please enter maximum 255 symbols"),
                "invalid": _("Invalid URL address")
            }}
        }


class TechnologySerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='id')
    label = serializers.CharField(source='technology_name')

    class Meta:
        model = Technology
        fields = ('value', 'label', 'color', 'specialization')


class SpecializationSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='id')
    label = serializers.CharField(source='specialization_name')

    class Meta:
        model = Specialization
        fields = ('value', 'label', 'technologies')


class HourlyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourlyRate
        fields = ['rate', 'currency']


class MonthlyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyRate
        fields = ['rate', 'currency']


class AverageHourlyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AverageHourlyRate
        fields = ['min_rate', 'max_rate', 'currency']


class CandidateProfileSerializer(NestedUpdateMixin, NestedCreateMixin,
                                 serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    communication_languages = serializers.MultipleChoiceField(
        choices=LANGUAGES,
        allow_empty=False)
    job_type = serializers.MultipleChoiceField(
        choices=JOB_TYPE,
        allow_empty=False)
    additional_links = CandidateLinkSerializer(many=True, required=False)
    hourly_rate = HourlyRateSerializer(required=False, allow_null=True)
    monthly_rate = MonthlyRateSerializer(required=False, allow_null=True)

    class Meta:
        model = CandidateProfile
        exclude = (
            'nationality_en',
            'job_position_en',
            'cover_letter_en',
            'adress_en',
            'city_en'
        )
        extra_kwargs = {
            "first_name": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}},
            "last_name": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}},
            "phone_number": {"error_messages": {"max_length": _("Please enter maximum 16 digits")}}
        }

    def validate_date_of_birth(self, value):
        FutureDateValidator.validate(self, date_of_birth=value)
        AgeRestrictionValidator.validate(self, date_of_birth=value)
        return value

    def validate_linkedin_url(self, value):
        LinkedinUrlValidator.validate(self, linkedin_url=value)
        return value

    def validate_phone_number(self, value):
        PnoneNumberValidator.validate(self, phone_number=value)
        return value

    def validate_image(self, value):
        FileSizeValidator.validate(self, file=value)
        ImageSizeValidator.validate(self, image=value)
        return value


class CandidateProfileRetrieveSerializer(CandidateProfileSerializer):
    technologies = TechnologySerializer(many=True, read_only=True)
    specialization = SpecializationSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta(CandidateProfileSerializer.Meta):
        ...

    def get_image(self, obj):
        return build_backend_url(obj.image.url) if obj.image else None


class SimilarCandidateSerializer(CandidateProfileRetrieveSerializer):
    job_type = serializers.MultipleChoiceField(choices=JOB_TYPE, allow_empty=False)
    technologies = TechnologySerializer(many=True, read_only=True)
    specialization = SpecializationSerializer(many=True, read_only=True)
    hourly_rate = HourlyRateSerializer(required=False, allow_null=True)
    monthly_rate = MonthlyRateSerializer(required=False, allow_null=True)

    class Meta:
        model = CandidateProfile
        fields = (
            "id",
            "job_type",
            "technologies",
            "hourly_rate",
            "monthly_rate",
            "job_position",
            "experience",
            "experience_level",
            "specialization",
        )


class ShortCandidateProfileSerializer(serializers.ModelSerializer):
    job_type = serializers.MultipleChoiceField(
        choices=JOB_TYPE,
        allow_empty=False)
    technologies = TechnologySerializer(many=True, read_only=True)
    specialization = SpecializationSerializer(many=True, read_only=True)
    hourly_rate = HourlyRateSerializer(required=False, allow_null=True)
    monthly_rate = MonthlyRateSerializer(required=False, allow_null=True)
    hiring_date = serializers.SerializerMethodField(read_only=True)
    similar_candidates = serializers.SerializerMethodField(method_name='get_similar_candidates')

    class Meta:
        model = CandidateProfile
        fields = (
            "id",
            "job_type",
            "technologies",
            "hourly_rate",
            "monthly_rate",
            "hiring_date",
            "job_position",
            "cover_letter",
            "experience",
            "experience_level",
            "communication_languages",
            "is_identified",
            "created",
            "modified",
            "specialization",
            "country",
            "similar_candidates"
        )

    def get_hiring_date(self, obj):
        user = self.context['request'].user
        if user.is_authenticated and user.user_type == 'COMPANY':
            try:
                candidate = user.company_profile.hired_candidates.filter(candidate=obj).first()
                return candidate.created
            except (ObjectDoesNotExist, AttributeError):
                return None

    def get_similar_candidates(self, obj):
        similar_positions = CandidateProfile.objects.filter(
            technologies__in=obj.technologies.all()).distinct().exclude(pk=obj.pk)[:3]
        return SimilarCandidateSerializer(similar_positions, many=True).data


class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        fields = '__all__'
        extra_kwargs = {
            "first_name": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}},
            "last_name": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}},
            "phone_number": {"error_messages": {"max_length": _("Please enter maximum 16 digits")}}
        }

    def validate_phone_number(self, value):
        PnoneNumberValidator.validate(self, phone_number=value)
        return value


class AgencyContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencyContactPerson
        fields = '__all__'
        extra_kwargs = {
            "first_name": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}},
            "last_name": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}},
            "phone_number": {"error_messages": {"max_length": _("Please enter maximum 16 digits")}}
        }

    def validate_phone_number(self, value):
        PnoneNumberValidator.validate(self, phone_number=value)
        return value


class CompanyProfileSerializer(NestedUpdateMixin, NestedCreateMixin,
                               serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    communication_languages = serializers.MultipleChoiceField(
        choices=LANGUAGES,
        allow_empty=False)
    additional_links = CompanyLinkSerializer(many=True, required=False)
    contact_persons = ContactPersonSerializer(many=True)
    technologies = TechnologySerializer(many=True, read_only=True)
    specialization = SpecializationSerializer(many=True, read_only=True)

    class Meta:
        model = CompanyProfile
        exclude = (
            'company_name_en',
            'company_adress_en',
            'city_en',
            'company_description_en',
            'industry_en'
        )
        extra_kwargs = {
            "company_name": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}},
            "company_adress": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}},
            "industry": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}},
            "company_website": {"error_messages": {"invalid": _("Invalid URL address")}}
        }

    def validate_company_logo(self, value):
        FileSizeValidator.validate(self, file=value)
        ImageSizeValidator.validate(self, image=value)
        return value


class CompanyProfileRetrieveSerializer(CompanyProfileSerializer):
    company_logo = serializers.SerializerMethodField()

    class Meta(CompanyProfileSerializer.Meta):
        ...

    def get_company_logo(self, obj):
        return build_backend_url(obj.company_logo.url) if obj.company_logo else None


class ShortCompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = (
            "id",
            "company_logo",
            "company_description",
            "company_size",
            "industry",
            "company_website",
            "country",
            "communication_languages"
        )


class AgencyProfileListSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True, read_only=True)
    specialization = SpecializationSerializer(many=True, read_only=True)
    average_hourly_rate = AverageHourlyRateSerializer(read_only=True)

    class Meta:
        model = AgencyProfile
        fields = (
            "id",
            "company_name",
            "average_hourly_rate",
            "specialization",
            "technologies",
            "number_of_specialists",
            "country",
        )


class ShortAgencyProfileSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True, read_only=True)
    specialization = SpecializationSerializer(many=True, read_only=True)
    average_hourly_rate = AverageHourlyRateSerializer(read_only=True)
    communication_languages = serializers.MultipleChoiceField(
        choices=LANGUAGES,
        allow_empty=False)
    hiring_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AgencyProfile
        fields = (
            "id",
            "company_name",
            "company_description",
            "average_hourly_rate",
            "specialization",
            "communication_languages",
            "technologies",
            "country",
            "number_of_specialists",
            "founded",
            "company_type",
            "hiring_date"
        )

    def get_hiring_date(self, obj):
        user = self.context['request'].user
        if user.is_authenticated and user.user_type == 'COMPANY':
            try:
                agency = user.company_profile.hired_agencies.filter(agency=obj).first()
                return agency.created
            except (ObjectDoesNotExist, AttributeError):
                return None


class AgencyProfileSerializer(NestedUpdateMixin, NestedCreateMixin,
                              serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    communication_languages = serializers.MultipleChoiceField(
        choices=LANGUAGES,
        allow_empty=False)
    additional_links = AgencyLinkSerializer(many=True, required=False)
    contact_persons = AgencyContactPersonSerializer(many=True)

    class Meta:
        model = AgencyProfile
        exclude = (
            'company_name_en',
            'company_adress_en',
            'city_en',
            'company_description_en',
        )
        extra_kwargs = {
            "company_name": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}},
            "company_adress": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}},
            "industry": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}},
            "company_website": {"error_messages": {"invalid": _("Invalid URL address")}}
        }

    def validate_company_logo(self, value):
        FileSizeValidator.validate(self, file=value)
        ImageSizeValidator.validate(self, image=value)
        return value

    def validate_phone_number(self, value):
        PnoneNumberValidator.validate(self, phone_number=value)
        return value


class AgencyProfileRetrieveSerializer(AgencyProfileSerializer):
    company_logo = serializers.SerializerMethodField()

    class Meta(AgencyProfileSerializer.Meta):
        ...

    def get_company_logo(self, obj):
        return build_backend_url(obj.company_logo.url) if obj.company_logo else None


class CheckEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        norm_email = value.lower()
        if User.objects.filter(email=norm_email).exists():
            raise serializers.ValidationError(
                _("This email has been already registered in our system.")
            )
        return norm_email


class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )


class EmployeeProfileSeializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EmployeeProfile
        fields = '__all__'

    def validate_phone_number(self, value):
        PnoneNumberValidator.validate(self, phone_number=value)
        return value

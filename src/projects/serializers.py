import os

from django.core import exceptions
from django.utils.translation import ugettext_lazy as _
from drf_writable_nested.serializers import NestedCreateMixin, NestedUpdateMixin
from rest_framework import serializers

from accounts.models import CompanyProfile, User
from accounts.serializers import (
    CompanyProfileSerializer,
    ShortCompanyProfileSerializer,
    SpecializationSerializer,
    TechnologySerializer,
)
from accounts.validators import FileSizeValidator
from base.languages.constants import COUNTRY_CHOICES

from .models import JOB_TYPE, LANGUAGES, Position, PositionDocument, Project, ProjectDocument, Salary
from .validators import MinMaxValueValidator


class SalarySerilizer(serializers.ModelSerializer):

    class Meta:
        model = Salary
        fields = '__all__'
        extra_kwargs = {
            "min_salary": {"error_messages": {"invalid": _("Please enter numbers")}},
            "max_salary": {"error_messages": {"invalid": _("Please enter numbers")}}
        }


class NestedPositionSerializer(NestedCreateMixin, NestedUpdateMixin,
                               serializers.ModelSerializer):
    company = serializers.SerializerMethodField('get_company')

    communication_languages = serializers.MultipleChoiceField(
        choices=LANGUAGES,
        allow_empty=False)
    job_type = serializers.MultipleChoiceField(
        choices=JOB_TYPE,
        allow_empty=False)
    salary = SalarySerilizer(allow_null=True, required=False)

    class Meta:
        model = Position
        exclude = (
            'position_title_en',
            'requirements_en',
            'offers_en'
        )

    def _set_company_serializer(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return CompanyProfileSerializer(read_only=True).data
        else:
            return ShortCompanyProfileSerializer(read_only=True).data

    def validate(self, data):
        salary_data = data.get('salary')
        if salary_data:
            max_salary = salary_data.get('max_salary')
            min_salary = salary_data.get('min_salary')
            errors = dict()
            try:
                MinMaxValueValidator.validate(self, min_salary, max_salary)
            except exceptions.ValidationError as e:
                errors['max_salary'] = list(e.messages)

            if errors:
                raise serializers.ValidationError(errors)

        return super(NestedPositionSerializer, self).validate(data)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['company'] = request.user.company_profile
        return super().create(validated_data)

    def get_company(self, obj):
        request = self.context.get('request')
        try:
            company = CompanyProfileSerializer(
                request.user.company_profile).data
        except (exceptions.ObjectDoesNotExist, AttributeError):
            company = None
        return company


class ProjectSerializer(NestedCreateMixin, NestedUpdateMixin,
                        serializers.ModelSerializer):

    class Meta:
        model = Project
        exclude = (
            'company',
            'project_name_en',
            'project_name_de',
            'project_description_en',
            'project_description_de',
            'location_en',
            'location_de'
        )
        extra_kwargs = {
            "project_name": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}},
            "location": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}}
        }


class ProjectCreateSetializer(NestedCreateMixin, NestedUpdateMixin,
                              serializers.ModelSerializer):
    positions = NestedPositionSerializer(many=True, required=False)

    class Meta:
        model = Project
        exclude = (
            'company',
            'project_name_en',
            'project_description_en',
            'location_en'
        )
        extra_kwargs = {
            "project_name": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}},
            "location": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}}
        }


class PositionCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = [
            'id',
            'company_logo',
            'company_name',
            'industry',
            'company_description',
        ]


class PositionListSerializer(NestedCreateMixin, NestedUpdateMixin,
                             serializers.ModelSerializer):
    communication_languages = serializers.MultipleChoiceField(
        choices=LANGUAGES)
    job_type = serializers.MultipleChoiceField(
        choices=JOB_TYPE)
    technologies = TechnologySerializer(many=True)
    specialization = SpecializationSerializer(many=True)

    class Meta:
        model = Position
        fields = (
            "id",
            "communication_languages",
            "job_type",
            "technologies",
            "position_title",
            "experience",
            "experience_level",
            "created",
            "modified",
            "offers",
            "requirements",
            "specialization",
            "country",
        )


class PositionCompanyListSerializer(PositionListSerializer):
    """
    Position serializer used only in company_positions view
    """
    project = serializers.SerializerMethodField(read_only=True)

    class Meta(PositionListSerializer.Meta):
        fields = PositionListSerializer.Meta.fields + ('project', )

    def get_project(self, obj):
        return str(obj.project.pk) if obj.project else None


class PositionRetrieveSerializer(serializers.ModelSerializer):
    company = PositionCompanySerializer(read_only=True)
    communication_languages = serializers.MultipleChoiceField(
        choices=LANGUAGES)
    job_type = serializers.MultipleChoiceField(
        choices=JOB_TYPE)
    project = ProjectSerializer(read_only=True)
    application_date = serializers.SerializerMethodField(read_only=True)
    technologies = TechnologySerializer(many=True)
    specialization = SpecializationSerializer(many=True)
    similar_jobs = serializers.SerializerMethodField(method_name='get_similar_jobs')

    class Meta:
        model = Position
        fields = (
            "id",
            "company",
            "communication_languages",
            "job_type",
            "project",
            "application_date",
            "technologies",
            "position_title",
            "experience",
            "experience_level",
            "requirements",
            "offers",
            "created",
            "modified",
            "specialization",
            "country",
            "similar_jobs"
        )

    def get_application_date(self, obj):
        candidate = None

        user = self.context['request'].user
        if user.user_type == User.USER_TYPE_CANDIDATE:
            candidate = self.context.get('candidate')
        elif user.user_type == User.USER_TYPE_AGENCY:
            candidate = self.context.get('agency')

        if not candidate:
            return None

        application = candidate.position_applications\
            .filter(position=obj).first()

        if not application:
            return None

        return application.created

    def get_similar_jobs(self, obj):
        similar_jobs = Position.objects.filter(
            technologies__in=obj.technologies.all()).distinct().exclude(pk=obj.pk)[:3]
        return PositionListSerializer(similar_jobs, many=True).data


class ShortPositionRetrieveSerializer(serializers.ModelSerializer):
    company = PositionCompanySerializer(read_only=True)
    communication_languages = serializers.MultipleChoiceField(
        choices=LANGUAGES)
    job_type = serializers.MultipleChoiceField(
        choices=JOB_TYPE)
    project = ProjectSerializer(read_only=True)
    technologies = TechnologySerializer(many=True)
    specialization = SpecializationSerializer(many=True)

    class Meta:
        model = Position
        exclude = (
            'position_title_en',
            'requirements_en',
            'offers_en',
            'salary'
        )


class PositionProjectSerializer(serializers.ModelSerializer):
    company = PositionCompanySerializer(read_only=True)
    communication_languages = serializers.MultipleChoiceField(
        choices=LANGUAGES)
    job_type = serializers.MultipleChoiceField(
        choices=JOB_TYPE)
    salary = SalarySerilizer(allow_null=True, required=False)

    class Meta:
        model = Position
        fields = '__all__'
        extra_kwargs = {
            "position_title": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}},
        }


class PositionSerializer(NestedCreateMixin, NestedUpdateMixin,
                         serializers.ModelSerializer):
    communication_languages = serializers.MultipleChoiceField(
        choices=LANGUAGES,
        allow_empty=False)
    job_type = serializers.MultipleChoiceField(
        choices=JOB_TYPE,
        allow_empty=False)
    salary = SalarySerilizer(allow_null=True, required=False)
    country = serializers.ChoiceField(choices=COUNTRY_CHOICES, required=True)

    class Meta:
        model = Position
        exclude = (
            'company',
            'position_title_en',
            'requirements_en',
            'offers_en'
        )
        extra_kwargs = {
            "position_title": {"error_messages": {"max_length": _("Please enter maximum 255 symbols")}},
        }

    def get_company(self, *args, **kwargs):
        request = self.context.get('request')
        try:
            company = request.user.company_profile
        except (exceptions.ObjectDoesNotExist, AttributeError):
            company = None
        return company

    def get_fields(self, *args, **kwargs):
        fields = super(PositionSerializer, self).get_fields(*args, **kwargs)
        fields['project'].queryset = fields['project'].queryset.filter(
            company=self.get_company())
        return fields

    def validate(self, data):
        salary_data = data.get('salary')
        if salary_data:
            max_salary = salary_data.get('max_salary')
            min_salary = salary_data.get('min_salary')
            errors = dict()
            try:
                MinMaxValueValidator.validate(self, min_salary, max_salary)
            except exceptions.ValidationError as e:
                errors['max_salary'] = list(e.messages)

            if errors:
                raise serializers.ValidationError(errors)

        return super(PositionSerializer, self).validate(data)


class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField(
        required=True,
        error_messages={
            "blank": _("This field is required")
        }
    )


class ProjectDocumentSerializer(serializers.ModelSerializer):
    document_name = serializers.SerializerMethodField('get_filename')

    class Meta:
        model = ProjectDocument
        fields = ['document', 'document_name']

    def validate_document(self, value):
        FileSizeValidator.validate(self, file=value)
        return value

    def get_filename(self, value):
        try:
            url = value.document.url
        except (AttributeError, ValueError):
            return None
        return os.path.basename(url)


class PositionDocumentSerializer(ProjectDocumentSerializer):

    class Meta:
        model = PositionDocument
        fields = ['document', 'document_name']

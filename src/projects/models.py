from django.core.validators import FileExtensionValidator, MinLengthValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from multiselectfield import MultiSelectField

from accounts.constants import EXPERIENCE, EXPERIENCE_LVL, JOB_TYPE, LANGUAGES
from accounts.models import AgencyProfile, CandidateProfile, CompanyProfile, Technology
from base.languages.constants import COUNTRY_AVAILABLE_CHOICES
from base.models import TimeStampedModel
from projects.constants import CURRENCIES


class Project(TimeStampedModel):
    company = models.ForeignKey(
        CompanyProfile,
        verbose_name=_('Company'),
        related_name='projects',
        on_delete=models.CASCADE)
    project_name = models.CharField(
        _('Project name'),
        max_length=255,
        blank=False)
    project_description = models.TextField(
        _('Project description'),
        validators=[MinLengthValidator(255, message=_("Please enter minimum 255 symbols"))],
        blank=False)
    location = models.CharField(
        _('Location'),
        max_length=255,
        blank=True)

    def __str__(self):
        return self.project_name


class Salary(TimeStampedModel):
    min_salary = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        blank=False)
    max_salary = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        blank=False)
    currency = models.CharField(
        choices=CURRENCIES,
        max_length=3,
        blank=False)


class Position(TimeStampedModel):
    company = models.ForeignKey(
        CompanyProfile,
        verbose_name=_('Company'),
        related_name='positions',
        on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project,
        verbose_name=_('Project'),
        related_name='positions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    position_title = models.CharField(
        _('Position title'),
        max_length=255,
        blank=False)
    technologies = models.ManyToManyField(
        Technology,
        related_name='position_technologies',
        db_index=True,
        blank=False)
    experience = models.IntegerField(
        _('Experience'),
        choices=EXPERIENCE,
        db_index=True,
        blank=False)
    experience_level = models.IntegerField(
        _('Experience level'),
        choices=EXPERIENCE_LVL,
        db_index=True,
        blank=False)
    job_type = MultiSelectField(
        _('Job type'),
        choices=JOB_TYPE,
        db_index=True,
        blank=False)
    communication_languages = MultiSelectField(
        _('Communication languages'),
        choices=LANGUAGES,
        db_index=True,
        blank=False)
    requirements = models.TextField(
        _('Requirements'),
        validators=[MinLengthValidator(255, message=_("Please enter minimum 255 symbols"))],
        blank=True,
        null=True)
    offers = models.TextField(
        _('What we offer'),
        validators=[MinLengthValidator(255, message=_("Please enter minimum 255 symbols"))],
        blank=True,
        null=True)
    salary = models.OneToOneField(
        Salary,
        related_name='position',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    specialization = models.ManyToManyField(
        'accounts.Specialization',
        related_name='positions',
        db_index=True,
        blank=False)
    country = models.CharField(
        _('Country'),
        choices=COUNTRY_AVAILABLE_CHOICES,
        max_length=255,
        db_index=True
    )

    def __str__(self):
        return f'{self.position_title}__<{self.company}>'


class CandidatePositionApplication(TimeStampedModel):
    candidate = models.ForeignKey(CandidateProfile,
                                  related_name='position_applications',
                                  null=False,
                                  blank=False,
                                  on_delete=models.CASCADE)
    position = models.ForeignKey(Position,
                                 related_name='candidate_applications',
                                 null=False,
                                 blank=False,
                                 on_delete=models.CASCADE)

    class Meta:
        unique_together = ('candidate', 'position')


class AgencyPositionApplication(TimeStampedModel):
    agency = models.ForeignKey(AgencyProfile,
                               related_name='position_applications',
                               null=False,
                               blank=False,
                               on_delete=models.CASCADE)
    position = models.ForeignKey(Position,
                                 related_name='agency_applications',
                                 null=False,
                                 blank=False,
                                 on_delete=models.CASCADE)

    class Meta:
        unique_together = ('agency', 'position')


class ProjectDocument(TimeStampedModel):
    company = models.ForeignKey(
        CompanyProfile,
        related_name='project_documents',
        on_delete=models.CASCADE
    )
    document = models.FileField(
        upload_to='project_documents',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx'])]
    )

    def __str__(self):
        return f'{self.company}_project_doc_<candidate_profile_id {self.company.pk}>'


class PositionDocument(TimeStampedModel):
    company = models.ForeignKey(
        CompanyProfile,
        related_name='position_documents',
        on_delete=models.CASCADE
    )
    document = models.FileField(
        upload_to='position_documents',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx'])]
    )

    def __str__(self):
        return f'{self.company}_position_doc_<candidate_profile_id {self.company.pk}>'

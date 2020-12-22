import random

from colorfield.fields import ColorField
from django.utils import timezone as django_timezone
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import FileExtensionValidator, MaxLengthValidator, MinLengthValidator, MinValueValidator
from django.db import models, transaction
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from guardian.mixins import GuardianUserMixin
from multiselectfield import MultiSelectField
from simple_history.models import HistoricalRecords

from accounts.constants import EXPERIENCE, EXPERIENCE_LVL, JOB_TYPE, LANGUAGES
from base.languages.constants import COUNTRY_CHOICES
from base.models import TimeStampedModel
from projects.constants import CURRENCIES


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        with transaction.atomic():
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, GuardianUserMixin, PermissionsMixin):
    USER_TYPE_COMPANY = 'COMPANY'
    USER_TYPE_CANDIDATE = 'CANDIDATE'
    USER_TYPE_AGENCY = 'AGENCY'
    USER_TYPE_EMPLOYEE = 'EMPLOYEE'
    USER_TYPE_CHOICES = (
        (USER_TYPE_COMPANY, 'Company'),
        (USER_TYPE_CANDIDATE, 'Candidate'),
        (USER_TYPE_AGENCY, 'Agency'),
        (USER_TYPE_EMPLOYEE, 'Employee')
    )

    EMPLOYEE_TYPE_ADMINISTRATOR = 'ADMINISTRATOR'
    EMPLOYEE_TYPE_MANAGER = 'MANAGER'
    EMPLOYEE_TYPE_HR = 'HR'
    EMPLOYEE_TYPE_CHOICES = (
        (EMPLOYEE_TYPE_ADMINISTRATOR, 'Administrator'),
        (EMPLOYEE_TYPE_MANAGER, 'Manager'),
        (EMPLOYEE_TYPE_HR, 'HR')
    )

    employer = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='employees',
        on_delete=models.CASCADE
    )
    employee_type = models.CharField(_('Employee type'), choices=EMPLOYEE_TYPE_CHOICES,
                                     max_length=32, null=True, blank=True, default=None)
    email = models.EmailField(
        _('Email address'),
        unique=True,
        error_messages={'unique': _("This email has been already registered in our system.")}
    )
    user_type = models.CharField(_('User type'), choices=USER_TYPE_CHOICES,
                                 default=USER_TYPE_CANDIDATE, max_length=32)
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('Is active'), default=False)
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    has_password = models.BooleanField(default=True)

    history = HistoricalRecords(user_db_constraint=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Membership
    membership_active = models.BooleanField(default=False)
    membership_activated_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    @cached_property
    def candidate(self):
        try:
            obj = self.candidate_profile
        except (ObjectDoesNotExist, AttributeError):
            return None

        return obj

    @cached_property
    def agency(self):
        try:
            obj = self.agency_profile
        except (ObjectDoesNotExist, AttributeError):
            return None

        return obj

    @cached_property
    def company(self):
        try:
            obj = self.company_profile
        except (ObjectDoesNotExist, AttributeError):
            return None

        return obj

    @cached_property
    def employee(self):
        try:
            obj = self.employee_profile
        except (ObjectDoesNotExist, AttributeError):
            return None

        return obj

    @cached_property
    def profile(self):
        return {
            self.USER_TYPE_CANDIDATE: self.candidate,
            self.USER_TYPE_COMPANY: self.company,
            self.USER_TYPE_AGENCY: self.agency,
            self.USER_TYPE_EMPLOYEE: self.employee,
        }.get(self.user_type)

    @cached_property
    def censored_phone_number(self):
        if not self.phone_number or \
                not self.mfa_methods.filter(is_active=True, name='sms').exists():
            return None

        return '*' * 9 + self.phone_number[-3:]

    @property
    def readable_employee_type(self):
        if self.user_type == 'EMPLOYEE':
            employee_types = {
                'ADMINISTRATOR': 'Administrator',
                'MANAGER': 'Manager',
                'HR': 'HR'
            }
            return employee_types.get(self.employee_type, None)
        return None

    @property
    def employer_organization_name(self):
        if self.user_type == 'EMPLOYEE':
            if self.employer.user_type == 'COMPANY':
                return self.employer.company.company_name
            if self.employer.user_type == 'AGENCY':
                return self.employer.agency.company_name
            return None

    def clean(self):
        if self.user_type == 'EMPLOYEE' and not self.employee_type:
            raise ValidationError(_('Employee type of user should have a role'))
        if self.user_type != 'EMPLOYEE' and self.employee_type:
            raise ValidationError(_('This type of user should not have a role'))
        if self.user_type != 'EMPLOYEE' and self.employer:
            raise ValidationError(_('Only employee type of user can have Employer'))

    def set_password(self, raw_password):
        self.has_password = True
        return super().set_password(raw_password)

    def activate_membership(self):
        if self.membership_active:
            return

        self.membership_active = True
        self.membership_activated_date = django_timezone.now()
        self.save()


class CandidateCV(TimeStampedModel):
    user = models.ForeignKey(
        User,
        related_name='candidate_cvs',
        on_delete=models.CASCADE
    )
    cv_file = models.FileField(
        upload_to='candidate_cvs',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )

    def __str__(self):
        return f'{self.user.email}_CV_<user_id {self.user.id}>'


class CompanyDocument(TimeStampedModel):
    user = models.ForeignKey(
        User,
        related_name='company_documents',
        on_delete=models.CASCADE
    )
    document = models.FileField(
        upload_to='company_documents',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx'])]
    )

    def __str__(self):
        return f'{self.user.email}__<user_id {self.user.id}>'


class CompanyProfile(TimeStampedModel):
    COMPANY_SIZE = (
        (1, '<50'),
        (2, '50-200'),
        (3, '200-500'),
        (4, '500+')
    )

    user = models.OneToOneField(
        User,
        related_name='company_profile',
        on_delete=models.CASCADE)
    company_logo = models.ImageField(
        _('Logo'),
        upload_to='company_logos',
        blank=True,
        null=True)
    company_name = models.CharField(
        _('Company name'),
        max_length=255,
        blank=False)
    company_adress = models.CharField(_('Adress'), max_length=255, blank=False)
    postal_code = models.CharField(_('Postal Code'), max_length=255, blank=False)
    city = models.CharField(_('City'), max_length=255, blank=False)
    country = models.CharField(
        _('Country'),
        choices=COUNTRY_CHOICES,
        max_length=255,
        blank=False,
        db_index=True
    )
    company_description = models.TextField(
        _('Description'),
        blank=True,
        validators=[MinLengthValidator(255, message=_("Please enter minimum 255 symbols"))])
    company_size = models.IntegerField(
        _('Company Size'),
        choices=COMPANY_SIZE,
        null=True)
    industry = models.CharField(_('Industry'), max_length=255, blank=True)
    company_website = models.CharField(
        _('Website'),
        max_length=255,
        blank=True)
    communication_languages = MultiSelectField(
        _('Communication languages'),
        choices=LANGUAGES,
        blank=False)

    class Meta:
        verbose_name = 'comany profile'
        verbose_name_plural = 'company profiles'

    def __str__(self):
        return self.company_name

    def get_contact_persons_email(self):
        contact_persons = self.contact_persons.all()
        return [cp.email for cp in contact_persons]


class ContactPerson(TimeStampedModel):
    company = models.ForeignKey(
        'CompanyProfile',
        verbose_name=_('Company'),
        null=True,
        related_name='contact_persons',
        on_delete=models.CASCADE)
    first_name = models.CharField(_('First name'), max_length=255, blank=False)
    last_name = models.CharField(_('Last name'), max_length=255, blank=False)
    phone_number = models.CharField(
        _('Phone number'),
        max_length=16,
        blank=False)
    email = models.EmailField(_('Email address'), blank=False)


class Link(TimeStampedModel):
    company = models.ForeignKey(
        'CompanyProfile',
        verbose_name=_('Company'),
        related_name='additional_links',
        on_delete=models.CASCADE)
    url = models.CharField(_('Link url'), max_length=255, blank=True)


def generate_random_color():
    return '#{:06x}'.format(random.randint(0, 256**3))


class Specialization(TimeStampedModel):
    specialization_name = models.CharField(
        _('Specialization name'),
        max_length=50,
        unique=True,
        blank=False
    )

    class Meta:
        verbose_name = 'specialization'
        verbose_name_plural = 'specializations'

    def __str__(self):
        return self.specialization_name


class Technology(TimeStampedModel):
    technology_name = models.CharField(
        _('Technology name'),
        max_length=50,
        unique=True,
        blank=False
    )
    specialization = models.ManyToManyField(
        Specialization,
        related_name='technologies',
    )
    color = ColorField(
        default=generate_random_color
    )

    class Meta:
        verbose_name = 'technology'
        verbose_name_plural = 'technologies'

    def __str__(self):
        return self.technology_name


class AverageHourlyRate(TimeStampedModel):
    min_rate = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        blank=False)
    max_rate = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        blank=False)
    currency = models.CharField(
        choices=CURRENCIES,
        max_length=3,
        blank=False)

    def __str__(self):
        return f'{self.min_rate}-{self.max_rate} {self.currency}'


class HourlyRate(TimeStampedModel):
    rate = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        blank=False)
    currency = models.CharField(
        choices=CURRENCIES,
        max_length=3,
        blank=False)

    def __str__(self):
        return f'{self.rate} {self.currency}'


class MonthlyRate(HourlyRate):
    pass


class CandidateProfile(TimeStampedModel):
    user = models.OneToOneField(
        User,
        related_name='candidate_profile',
        on_delete=models.CASCADE)
    first_name = models.CharField(
        _('First name'),
        max_length=255,
        blank=False,
        error_messages={
            "max_length": _("Please enter maximum 255 symbols")
        })
    last_name = models.CharField(
        _('Last name'),
        max_length=255,
        blank=False,
        error_messages={
            "max_length": _("Please enter maximum 255 symbols")
        })
    nationality = models.CharField(_('Nationality'), max_length=255, blank=False)
    image = models.ImageField(
        _('Profile image'),
        upload_to='candidate_images',
        blank=True,
        null=True)
    job_position = models.CharField(
        _('Job position'),
        max_length=255,
        blank=False)
    cover_letter = models.TextField(
        _('Cover letter'),
        validators=[
            MinLengthValidator(255, message=_("Please enter between 255 and 1000 symbols")),
            MaxLengthValidator(1000, message=_("Please enter between 255 and 1000 symbols")),
        ],
        blank=True,
        null=True)
    hourly_rate = models.OneToOneField(
        HourlyRate,
        related_name='hourly_rate',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    monthly_rate = models.OneToOneField(
        MonthlyRate,
        related_name='monthly_rate',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    adress = models.CharField(_('Adress'), max_length=255, blank=False)
    postal_code = models.CharField(_('Postal Code'), max_length=255, blank=False)
    city = models.CharField(_('City'), max_length=255, blank=False)
    country = models.CharField(
        _('Country'),
        choices=COUNTRY_CHOICES,
        max_length=255,
        blank=False,
        db_index=True
    )
    date_of_birth = models.DateField(_('Date of birth'), blank=False)
    experience = models.IntegerField(
        _('Experience'),
        choices=EXPERIENCE,
        blank=False,
        db_index=True
    )
    experience_level = models.IntegerField(
        _('Experience level'),
        choices=EXPERIENCE_LVL,
        blank=False,
        db_index=True,
    )
    job_type = MultiSelectField(
        _('Job type'),
        choices=JOB_TYPE,
        blank=False,
        db_index=True
    )
    specialization = models.ManyToManyField(
        'Specialization',
        related_name='candidate_specilaizations',
        blank=False)
    technologies = models.ManyToManyField(
        'Technology',
        related_name='technologies',
        blank=False,
        db_index=True
    )
    communication_languages = MultiSelectField(
        _('Communication Language'),
        choices=LANGUAGES,
        blank=False)
    phone_number = models.CharField(
        _('Phone number'),
        max_length=16,
        blank=False)
    email = models.EmailField(_('Email address'), blank=False)
    linkedin_url = models.URLField(
        _('LinkedIn Profile'),
        blank=True,
        null=True)
    is_identified = models.BooleanField(_('Is identified'), default=False)

    def __str__(self):
        return self.user.email

    @cached_property
    def full_name(self):
        return "{} {}".format(self.first_name,
                              self.last_name)


class CandidateLink(TimeStampedModel):
    candidate = models.ForeignKey(
        'CandidateProfile',
        verbose_name=_('Candidate'),
        related_name='additional_links',
        on_delete=models.CASCADE)
    url = models.CharField(_('Link url'), max_length=255, blank=True)


class CandidateHiring(TimeStampedModel):
    company = models.ForeignKey(
        CompanyProfile,
        related_name='hired_candidates',
        on_delete=models.CASCADE)
    candidate = models.ForeignKey(
        CandidateProfile,
        related_name='hiring_companies',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('company', 'candidate')


class AgencyQuerySet(models.QuerySet):

    def filter_active(self):
        """
        Returns QuerySet with only active agency profiles
        """
        return self.filter(user__membership_active=True)

    def filter_active_or_owner(self, agency):
        """
        Returns QuerySet with only active agency profiles
        or are owned by specific agency
        """
        return self.filter(
            models.Q(user__membership_active=True) | models.Q(pk=agency.pk)
        )


class AgencyManager(models.Manager):

    def get_queryset(self):
        return AgencyQuerySet(self.model, using=self._db)

    def filter_active(self):
        return self.get_queryset().filter_active()

    def filter_active_or_owner(self, agency):
        return self.get_queryset().filter_active_or_owner(agency)


class AgencyProfile(TimeStampedModel):
    NUMBER_OF_SPECIALISTS = (
        (1, '<5'),
        (2, '5-10'),
        (3, '10-20'),
        (4, '>20')
    )

    user = models.OneToOneField(
        User,
        related_name='agency_profile',
        on_delete=models.CASCADE)
    company_logo = models.ImageField(
        _('Logo'),
        upload_to='company_logos',
        blank=True,
        null=True)
    company_name = models.CharField(
        _('Company name'),
        max_length=255,
        blank=False)
    number_of_specialists = models.IntegerField(
        _('Number of available specialists'),
        choices=NUMBER_OF_SPECIALISTS,
        null=True)
    communication_languages = MultiSelectField(
        _('Communication languages'),
        choices=LANGUAGES,
        blank=False)
    company_description = models.TextField(
        _('Description'),
        blank=True,
        validators=[
            MinLengthValidator(100, message=_("Please enter minimum 100 symbols")),
            MaxLengthValidator(2000, message=_("Please enter maximun 2000 symbols"))
        ]
    )
    founded = models.DateField(_('Founded'), blank=False)
    company_type = models.CharField(_('Company type'), max_length=255, blank=False)
    average_hourly_rate = models.OneToOneField(
        'AverageHourlyRate',
        related_name='average_hourly_rate',
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    specialization = models.ManyToManyField(
        'Specialization',
        related_name='agency_specilaizations',
        blank=False)
    technologies = models.ManyToManyField(
        'Technology',
        related_name='agency_technologies',
        blank=False)
    company_adress = models.CharField(_('Adress'), max_length=255, blank=False)
    postal_code = models.CharField(_('Postal Code'), max_length=255, blank=False)
    city = models.CharField(_('City'), max_length=255, blank=False)
    country = models.CharField(
        _('Country'),
        choices=COUNTRY_CHOICES,
        max_length=255,
        blank=False,
        db_index=True
    )
    company_website = models.CharField(
        _('Website'),
        max_length=255)
    phone_number = models.CharField(
        _('Phone number'),
        max_length=16,
        blank=False)

    objects = AgencyManager()

    class Meta:
        verbose_name = 'agency profile'
        verbose_name_plural = 'agency profiles'

    def __str__(self):
        return self.company_name

    def get_contact_persons_email(self):
        contact_persons = self.contact_persons.all()
        return [cp.email for cp in contact_persons]

    def activate_membership(self):
        self.user.activate_membership()


class AgencyHiring(TimeStampedModel):
    company = models.ForeignKey(
        CompanyProfile,
        related_name='hired_agencies',
        on_delete=models.CASCADE)
    agency = models.ForeignKey(
        AgencyProfile,
        related_name='hiring_companies',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('company', 'agency')


class AgencyLink(TimeStampedModel):
    company = models.ForeignKey(
        'AgencyProfile',
        verbose_name=_('Company'),
        related_name='additional_links',
        on_delete=models.CASCADE)
    url = models.CharField(_('Link url'), max_length=255, blank=True)


class AgencyContactPerson(TimeStampedModel):
    company = models.ForeignKey(
        'AgencyProfile',
        verbose_name=_('Company'),
        null=True,
        related_name='contact_persons',
        on_delete=models.CASCADE)
    first_name = models.CharField(_('First name'), max_length=255, blank=False)
    last_name = models.CharField(_('Last name'), max_length=255, blank=False)
    phone_number = models.CharField(
        _('Phone number'),
        max_length=16,
        blank=False)
    email = models.EmailField(_('Email address'), blank=False)


class AgencyCandidateCV(TimeStampedModel):
    user = models.ForeignKey(
        User,
        related_name='agency_candidate_cvs',
        on_delete=models.CASCADE
    )
    cv_file = models.FileField(
        upload_to='agency_candidate_cvs',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )

    def __str__(self):
        return f'{self.user.email}_agency_candidate_CV_<user_id {self.user.id}>'


class EmployeeProfile(TimeStampedModel):
    user = models.OneToOneField(
        User,
        related_name='employee_profile',
        on_delete=models.CASCADE)
    first_name = models.CharField(_('First name'), max_length=255, blank=False)
    last_name = models.CharField(_('Last name'), max_length=255, blank=False)
    position = models.CharField(_('Position at company'), max_length=255, blank=False)
    phone_number = models.CharField(
        _('Phone number'),
        max_length=16,
        blank=False)
    email = models.EmailField(_('Email address'), blank=False)

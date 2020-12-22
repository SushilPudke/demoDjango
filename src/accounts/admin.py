from admin_reports import Report, register
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminSplitDateTime, FilteredSelectMultiple
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
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


class SpecializationAdminForm(forms.ModelForm):
    technologies = forms.ModelMultipleChoiceField(
        queryset=Technology.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Tehcnologies'),
            is_stacked=False
        )
    )

    class Meta:
        fields = '__all__'
        model = Specialization

    def __init__(self, *args, **kwargs):
        super(SpecializationAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['technologies'].initial = self.instance.technologies.all()

    def save(self, commit=True):
        specialization = super(SpecializationAdminForm, self).save(commit=False)

        if commit:
            specialization.save()

        if specialization.pk:
            technologies_data = self.cleaned_data['technologies']
            for technology in technologies_data.iterator():
                specialization.technologies.add(technology)
            self.save_m2m()

        return specialization


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    form = SpecializationAdminForm


class UserReportForm(forms.Form):
    start_date = forms.SplitDateTimeField(label=mark_safe("<br/>Start Date"), widget=AdminSplitDateTime())
    end_date = forms.SplitDateTimeField(label=mark_safe("<br/>End Date"), widget=AdminSplitDateTime())


@register()
class UsersReport(Report):
    form_class = UserReportForm

    def aggregate(self, start_date=None, end_date=None, **kwargs):
        created = User.history.filter(history_type='+', history_date__range=[start_date, end_date]).count()
        deleted = User.history.filter(history_type='-', history_date__range=[start_date, end_date]).count()
        return [{
            'Created users': created,
            'Deleted users': deleted
        }]


class TechnologyResource(resources.ModelResource):
    class Meta:
        model = Technology
        import_id_fields = ('id', 'technology_name')
        exclude = ('created', 'modified')
        search_fields = ('technology_name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'id', 'phone_number')
    search_fields = ('email', 'phone_number')
    change_list_template = "admin/change_list.html"


@admin.register(CandidateCV)
class CandidateCVAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'user_id', 'id', 'created', 'modified')
    search_fields = ('user__email',)


@admin.register(CompanyDocument)
class CompanyDocumentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'user_id', 'id', 'created', 'modified')
    search_fields = ('user__email',)


@admin.register(AverageHourlyRate)
class AverageHourlyRateAdmin(admin.ModelAdmin):
    pass


@admin.register(HourlyRate)
class HourlyRateAdmin(admin.ModelAdmin):
    pass


@admin.register(MonthlyRate)
class MonthlyRateAdmin(admin.ModelAdmin):
    pass


class ContactPersonInlineAdmin(admin.TabularInline):
    model = ContactPerson
    extra = 1


class AgencyContactPersonInlineAdmin(admin.TabularInline):
    model = AgencyContactPerson
    extra = 1


class LinkInlineAdmin(admin.TabularInline):
    model = Link
    extra = 1


class AgencyLinkInlineAdmin(admin.TabularInline):
    model = AgencyLink
    extra = 1


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    inlines = [
        ContactPersonInlineAdmin,
        LinkInlineAdmin
    ]
    search_fields = ('company_name',)
    exclude = (
        'company_name_en',
        'company_adress_en',
        'city_en',
        'country_en',
        'company_description_en',
        'industry_en'
    )


@admin.register(AgencyProfile)
class AgencyProfileAdmin(admin.ModelAdmin):
    inlines = [
        AgencyContactPersonInlineAdmin,
        AgencyLinkInlineAdmin
    ]
    search_fields = ('company_name',)
    exclude = (
        'company_name_en',
        'company_adress_en',
        'city_en',
        'country_en',
        'company_description_en'
    )


class CandidateLinkInlineAdmin(admin.TabularInline):
    model = CandidateLink
    extra = 1


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'pk', 'full_name', 'is_identified')
    search_fields = ('user__email',)
    list_filter = ('is_identified',)
    inlines = [
        CandidateLinkInlineAdmin,
    ]
    exclude = (
        'nationality_en',
        'job_position_en',
        'cover_letter_en',
        'adress_en',
        'city_en',
        'country_en'
    )


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'pk', 'first_name', 'last_name', 'position')


@admin.register(Technology)
class TechnologyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = TechnologyResource
    list_display = ('technology_name', 'color')
    filter_horizontal = ['specialization']

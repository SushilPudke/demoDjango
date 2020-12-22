from celeryapp import app
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from .models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


@app.task
def daily_users_report():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    created = User.history.filter(history_type='+', history_date__range=[start_date, end_date])
    created_companies = created.filter(user_type="COMPANY").count()
    created_candidates = created.filter(user_type="CANDIDATE").count()
    created = created.count()
    deleted = User.history.filter(history_type='-', history_date__range=[start_date, end_date]).count()
    queryset = User.objects.filter()
    total_amount = queryset.count()
    companies_amount = queryset.filter(user_type="COMPANY").count()
    candiddates_amount = queryset.filter(user_type="CANDIDATE").count()
    unacivated_users = queryset.filter(is_active=False, date_joined__range=[start_date, end_date]).count()
    send_mail(
        subject=_('Daily users report'),
        message=_("Daily users report {8} - {9}:\n\n"
                  "New subscribtions:\n"
                  "\tTotal - {0}\n"
                  "\tCreated candidates - {1}\n"
                  "\tCreated companies - {2}\n"
                  "\tNot activated users - {4}\n\n"
                  "Deleted users - {3}\n\n"
                  "Total amount of users - {5}\n"
                  "\tCompanies - {6}\n"
                  "\tCandidates - {7}\n"
                  ).format(created, created_candidates, created_companies,
                           deleted, unacivated_users, total_amount,
                           companies_amount, candiddates_amount,
                           start_date, end_date),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.REPORTS_EMAIL],
    )


@app.task
def weekly_users_report():
    end_date = datetime.now()
    start_date = end_date - relativedelta(weeks=1)
    created = User.history.filter(history_type='+', history_date__range=[start_date, end_date])
    created_companies = created.filter(user_type="COMPANY").count()
    created_candidates = created.filter(user_type="CANDIDATE").count()
    created = created.count()
    deleted = User.history.filter(history_type='-', history_date__range=[start_date, end_date]).count()
    queryset = User.objects.filter()
    total_amount = queryset.count()
    companies_amount = queryset.filter(user_type="COMPANY").count()
    candiddates_amount = queryset.filter(user_type="CANDIDATE").count()
    unacivated_users = queryset.filter(is_active=False, date_joined__range=[start_date, end_date]).count()
    send_mail(
        subject=_('Monthly users report'),
        message=_("Monthly users report {8} - {9}:\n\n"
                  "New subscribtions:\n"
                  "\tTotal - {0}\n"
                  "\tCreated candidates - {1}\n"
                  "\tCreated companies - {2}\n"
                  "\tNot activated users - {4}\n\n"
                  "Deleted users - {3}\n\n"
                  "Total amount of users - {5}\n"
                  "\tCompanies - {6}\n"
                  "\tCandidates - {7}\n"
                  ).format(created, created_candidates, created_companies,
                           deleted, unacivated_users, total_amount,
                           companies_amount, candiddates_amount,
                           start_date, end_date),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.REPORTS_EMAIL],
    )


@app.task
def monthly_users_report():
    end_date = datetime.now()
    start_date = end_date - relativedelta(months=1)
    created = User.history.filter(history_type='+', history_date__range=[start_date, end_date])
    created_companies = created.filter(user_type="COMPANY").count()
    created_candidates = created.filter(user_type="CANDIDATE").count()
    created = created.count()
    deleted = User.history.filter(history_type='-', history_date__range=[start_date, end_date]).count()
    queryset = User.objects.filter()
    total_amount = queryset.count()
    companies_amount = queryset.filter(user_type="COMPANY").count()
    candiddates_amount = queryset.filter(user_type="CANDIDATE").count()
    unacivated_users = queryset.filter(is_active=False, date_joined__range=[start_date, end_date]).count()
    send_mail(
        subject=_('Monthly users report'),
        message=_("Monthly users report {8} - {9}:\n\n"
                  "New subscribtions:\n"
                  "\tTotal - {0}\n"
                  "\tCreated candidates - {1}\n"
                  "\tCreated companies - {2}\n"
                  "\tNot activated users - {4}\n\n"
                  "Deleted users - {3}\n\n"
                  "Total amount of users - {5}\n"
                  "\tCompanies - {6}\n"
                  "\tCandidates - {7}\n"
                  ).format(created, created_candidates, created_companies,
                           deleted, unacivated_users, total_amount,
                           companies_amount, candiddates_amount,
                           start_date, end_date),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.REPORTS_EMAIL],
    )


@app.task
def year_users_report():
    end_date = datetime.now()
    start_date = end_date - relativedelta(years=1)
    created = User.history.filter(history_type='+', history_date__range=[start_date, end_date])
    created_companies = created.filter(user_type="COMPANY").count()
    created_candidates = created.filter(user_type="CANDIDATE").count()
    created = created.count()
    deleted = User.history.filter(history_type='-', history_date__range=[start_date, end_date]).count()
    queryset = User.objects.filter()
    total_amount = queryset.count()
    companies_amount = queryset.filter(user_type="COMPANY").count()
    candiddates_amount = queryset.filter(user_type="CANDIDATE").count()
    unacivated_users = queryset.filter(is_active=False, date_joined__range=[start_date, end_date]).count()
    send_mail(
        subject=_('Year users report'),
        message=_("Year users report {8} - {9}:\n\n"
                  "New subscribtions:\n"
                  "\tTotal - {0}\n"
                  "\tCreated candidates - {1}\n"
                  "\tCreated companies - {2}\n"
                  "\tNot activated users - {4}\n\n"
                  "Deleted users - {3}\n\n"
                  "Total amount of users - {5}\n"
                  "\tCompanies - {6}\n"
                  "\tCandidates - {7}\n"
                  ).format(created, created_candidates, created_companies,
                           deleted, unacivated_users, total_amount,
                           companies_amount, candiddates_amount,
                           start_date, end_date),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.REPORTS_EMAIL],
    )

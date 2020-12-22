from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.template import loader
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from accounts.declared_signals import post_profile_activate
from accounts.models import AgencyProfile, CompanyProfile, CandidateProfile, User
from payments.declared_signals import post_membership_activate


@receiver(post_save, sender=AgencyProfile)
@receiver(post_save, sender=CompanyProfile)
@receiver(post_save, sender=CandidateProfile)
def profile_save_check_profile_activated(sender, created=False, instance: User = None, *args, **kwargs):
    user = instance.user

    if not created:
        return

    # If created agency profile but membership is not purchased
    if sender == AgencyProfile and not user.membership_active:
        return

    post_profile_activate.send(sender=sender, user=user)


@receiver(post_membership_activate)
def membership_activate_check_profile_activated(sender, user: User, *args, **kwargs):
    if not user.profile:
        return

    post_profile_activate.send(sender=sender, user=user)


@receiver(post_profile_activate, sender=AgencyProfile)
def agency_profile_activation(sender, user: User, *args, **kwargs):
    send_agency_profile_activation_mail(user)


def send_agency_profile_activation_mail(user: User):
    html_message = loader.render_to_string(
        'agency/profile_published.html',
        {'profile': user.agency}
    )

    send_mail(_('Your profile was published'),
              _('Your profile was published'),
              settings.EMAIL_HOST_USER,
              [user.email],
              html_message=html_message)

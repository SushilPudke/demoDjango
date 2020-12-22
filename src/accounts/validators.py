import re
import datetime

from django.utils.translation import ugettext_lazy as _
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError


class UppercaseValidator:
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter"),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _("The password must contain at least 1 uppercase letter")


class AgeRestrictionValidator:
    def validate(self, date_of_birth):
        delta = datetime.date.today().year - date_of_birth.year
        if delta < 16:
            raise ValidationError(
                _("Your age must be over 16")
            )

    def get_help_text(self):
        return _("Your age must be over 16")


class FutureDateValidator:
    def validate(self, date_of_birth):
        if date_of_birth > datetime.date.today():
            raise ValidationError(
                _("The date must not be in the future")
            )

    def get_help_text(self):
        return _("The date must not be in the future")


class LinkedinUrlValidator:
    def validate(self, linkedin_url):
        if linkedin_url != "" and linkedin_url is not None:
            if not re.findall("^(http(s)?:\\/\\/)?([\\w]+\\.)?linkedin\\.com\\/(pub|in|profile)", linkedin_url):
                raise ValidationError(
                    _("The link must contain a LinkedIn profile url")
                )

    def get_help_text(self):
        return _("The link must contain a LinkedIn profile url")


class PnoneNumberValidator:
    def validate(self, phone_number):
        if not re.match("^\\+\\d{9,15}$", phone_number):
            raise ValidationError(
                _("Phone number must be entered in the format +999999999")
            )

    def get_help_text(self):
        return _("Phone number must be entered in the format +999999999")


class FileSizeValidator:
    def validate(self, file):
        if file and file.size > 5242880:
            raise ValidationError(_("The file size must be maximum 5 MB"))

    def get_help_text(self):
        return _("The file size must be maximum 5 MB")


class ImageSizeValidator:
    def validate(self, image):
        if image:
            w, h = get_image_dimensions(image)
            if w < 400 or h < 400:
                raise ValidationError(_("The image must be at least 400x400px"))

    def get_help_text(self):
        return _("The image must be at least 400x400px")

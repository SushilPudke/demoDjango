from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import ValidationError


class ChangeFieldValidator:
    def validate(self, field):
        obj = self.get_object()
        field_object = obj._meta.get_field(field)
        field_value = field_object.value_from_object(obj)
        if field_value:
            raise ValidationError({
                field: _("This field can't be changed"),
            })

    def get_help_text(self):
        return _("Saved fields can't be changed")

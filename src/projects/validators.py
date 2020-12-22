from django.core.exceptions import ValidationError


class MinMaxValueValidator:
    def validate(self, min_salary, max_salary):
        if min_salary > max_salary:
            raise ValidationError(
                "Maximum salary is smaller than minimum salary"
            )

    def get_help_text(self):
        return "Maximum salary is smaller than minimum salary"

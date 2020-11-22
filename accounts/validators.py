import re

from django.core.exceptions import ValidationError


class NumberValidator(object):

    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                ('Twoje hasło musi zawierać co najmniej 1 cyfrę, 0–9.'),
                code='password_no_number',
            )

    def get_help_text(self):
        return (
            'Twoje hasło musi zawierać co najmniej 1 cyfrę, 0–9.'
        )


class UppercaseValidator(object):

    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                ('Twoje hasło musi zawierać co najmniej 1 wielką literę A-Z.'),
                code='password_no_upper',
            )

    def get_help_text(self):
        return (
            'Twoje hasło musi zawierać co najmniej 1 wielką literę A-Z.'
        )


class LowercaseValidator(object):

    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                ('Twoje hasło musi zawierać co najmniej 1 małą literę, a-z.'),
                code='password_no_lower',
            )

    def get_help_text(self):
        return (
            'Twoje hasło musi zawierać co najmniej 1 małą literę, a-z.'
        )

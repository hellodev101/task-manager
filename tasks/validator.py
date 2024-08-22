from typing import Any
from django import forms
from django.core.validators import EmailValidator

email_validator = EmailValidator(message="One or more email addresses are not valid")

class EmailListField(forms.CharField):
    def to_python(self, value): 
        "Normalize data to a list of strings"
        # Return an empty list of no input was given
        if not value:
            return []
        return [email.strip() for email in value.split(',')]
    
    def validate(self, value):
        "Cehck if value consists only of valid emails"
        super().validate(value)
        for email in value:
            email_validator(email)
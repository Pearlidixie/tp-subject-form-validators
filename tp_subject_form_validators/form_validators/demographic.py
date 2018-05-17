from django.apps import apps as django_apps
from django import forms

from edc_form_validators import FormValidator


class DemographicFormValidator(FormValidator):

    def clean(self):

        self.required_if(
                'Married',
                field='marital_status',
                field_required='number_wives')

        if (self.cleaned_data.get('marital_status') == "Single" and
                self.cleaned_data.get('is_married_citizen') == "No"):
            raise forms.ValidationError(
                'one has to be a citizen if not must be married to'
                ' a Motswana and have documents')

        if self.is_citizen == "No" and self.is_married_citizen == "Yes":
            if self.marriage_proof == "No":
                raise forms.ValidationError(
                    'one has to be a citizen if not must be married to'
                    ' a Motswana and have documents')

        if self.is_literate == "No" and self.literate_witness_avail == "No":
            raise forms.ValidationError(
                 'Must be literate or have a witness available')

        if self.is_minor == "Yes" and self.guardian_available == "No":
            raise forms.ValidationError(
                 'Should not be a minor or have a guardian available')



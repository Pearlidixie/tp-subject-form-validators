from django.apps import apps as django_apps
from django import forms
from tp_screening.models.subject_screening import SubjectScreening
from tp_screening.forms.subject_screening_form import SubjectScreeningForm
from edc_form_validators import FormValidator


class SubjectScreeningFormValidator(FormValidator):

    def clean(self):
        self.gender = self.cleaned_data.get('gender')
        self.is_citizen = self.cleaned_data.get('is_citizen')
        self.is_married_citizen = self.cleaned_data.get('is_married_citizen')
        self.marriage_proof = self.cleaned_data.get('marriage_proof')
        self.is_literate = self.cleaned_data.get('is_literate')
        self.literate_witness_avail = self.cleaned_data.get('literate_witness_avail')
        self.is_minor = self.cleaned_data.get('is_minor')
        self.guardian_available = self.cleaned_data.get('guardian_available')

        if (self.cleaned_data.get('is_citizen') == "No" and
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



from dateutil.relativedelta import relativedelta
from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import ABNORMAL, NO
from edc_form_validators import FormValidator


class SubjectConsentFormValidator(FormValidator):

    subject_screening_model = 'tp_screening.subjectscreening'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dob = self.cleaned_data.get('dob')
        self.consent_datetime = self.cleaned_data.get('consent_datetime')
        self.guardian_name = self.cleaned_data.get('guardian_name')
        self.screening_identifier = self.cleaned_data.get(
            'screening_identifier')

    @property
    def subject_screening_model_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    def clean(self):
        try:
            subject_screening = self.subject_screening_model_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                'Complete the "Subject Screening" form before proceeding.',
                code='missing_subject_screening')

        if self.add_form and not self.consent_datetime:
            raise forms.ValidationError(
                {'consent_datetime': 'This field is required.'})

        screening_age_in_years = relativedelta(
            subject_screening.report_datetime.date(), self.dob).years
        if screening_age_in_years != subject_screening.age_in_years:
            raise forms.ValidationError(
                {'dob':
                 'Age mismatch. The date of birth entered does not match the age at '
                 f'screening. Expected {subject_screening.age_in_years}. '
                 f'Got {screening_age_in_years}.'})

        condition = (
            self.cleaned_data.get('is_literate') == NO)
        self.required_if_true(
            condition=condition, field_required='witness_name')

        if(self.cleaned_data.get('identity') !=
           self.cleaned_data.get('confirm_identity')):
            raise forms.ValidationError(
                {'confirm_identity':
                 '\'Identity\' must match \'confirm_identity\''})


from dateutil.relativedelta import relativedelta
from django import forms
from django.test import TestCase
from edc_base.utils import get_utcnow

from tp_subject_form_validators.form_validators.subject_consent import (
    SubjectConsentFormValidator)
from tp_screening.models.subject_screening import SubjectScreening
from edc_constants.constants import NO


class TestSubjectConsentForm(TestCase):

    def setUp(self):
        self.screening_identifier = 'ABCDEF'
        self.subject_screening = SubjectScreening.objects.create(
            screening_identifier=self.screening_identifier, age_in_years=20)
        subject_screening_model = SubjectConsentFormValidator.subject_screening_model
        subject_screening_model = subject_screening_model.replace(
            'ambition_screening', 'ambition_validators')
        SubjectConsentFormValidator.subject_screening_model = subject_screening_model

    def test_subject_screening_ok(self):
        cleaned_data = dict(
            screening_identifier=self.subject_screening.screening_identifier,
            consent_datetime=get_utcnow(),
            dob=(get_utcnow() - relativedelta(years=20)).date())
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_no_subject_screening_invalid(self):
        """Check if there is was subject screening form for the participant"""
        cleaned_data = dict(
            consent_datetime=get_utcnow(),
            dob=(get_utcnow() - relativedelta(years=20)).date())
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(forms.ValidationError, form_validator.validate)
        self.assertIn('missing_subject_screening', form_validator._error_codes)

    def test_consent_datetime(self):
        dob = (get_utcnow() - relativedelta(years=20)).date()
        cleaned_data = dict(
            screening_identifier=self.subject_screening.screening_identifier,
            dob=dob)
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(forms.ValidationError, form_validator.validate)
        self.assertIn('consent_datetime', form_validator._errors)

        cleaned_data.update(consent_datetime=get_utcnow())
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_consent_age_mismatch_with_screening_age_invalid(self):
        """test if the age for the participant entered at screening
           matches the date of birth"""
        age_in_years = 18
        dob = (get_utcnow() - relativedelta(years=age_in_years)).date()
        cleaned_data = dict(
            dob=dob,
            screening_identifier=self.subject_screening.screening_identifier,
            consent_datetime=get_utcnow())
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(forms.ValidationError, form_validator.validate)
        self.assertIn('dob', form_validator._errors)

    def test_literate_witness_avail(self):
        """If participant is illeterate, that there should be a
           literate witness"""
        is_literate = NO
        cleaned_data = dict(
            screening_identifier=self.subject_screening.screening_identifier,
            consent_datetime=get_utcnow(),
            dob=(get_utcnow() - relativedelta(years=20)).date(),
            is_literate=is_literate,
            witness_name=None)
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(forms.ValidationError, form_validator.validate)
        self.assertIn('witness_name', form_validator._errors)

    def test_identy_match_confirm_identity(self):
        """Identity number in the identity field should match the one in
           confirm identity"""
        cleaned_data = dict(
            screening_identifier=self.subject_screening.screening_identifier,
            consent_datetime=get_utcnow(),
            dob=(get_utcnow() - relativedelta(years=20)).date(),
            identity=123455678,
            confirm_identity=12346789)
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(forms.ValidationError, form_validator.validate)
        self.assertIn('confirm_identity', form_validator._errors)



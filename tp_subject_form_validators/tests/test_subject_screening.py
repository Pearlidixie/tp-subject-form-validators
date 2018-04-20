from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from django import forms


from tp_subject_form_validators.form_validators.subject_screening import SubjectScreeningFormValidator
from datetime import date


class TestSubjectScreeningFormValidator(TestCase):

    def setUp(self):
        #super(TestSubjectScreeningFormValidator, self).setUp()
        #subject_screening_model = SubjectScreeningFormValidator.subject_screening_model

        self.options = {
            'report_datetime': date.today(),
            'gender': 'Female',
            'is_citizen': 'Yes',
            'is_married_citizen': 'N/A',
            'marriage_proof': 'N/A',
            'is_literate': 'Yes',
            'literate_witness_avail': 'N/A',
            'is_minor': 'No',
            'guardian_available': 'N/A',}

    def test_not_citizen_married(self):
        self.options['is_citizen'] = 'No'
        self.options['is_married_citizen'] = 'No'
        form_validator = SubjectScreeningFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_married_citizen_documents(self):
        self.options['is_citizen'] = 'No'
        self.options['is_married_citizen'] = 'No'
        form_validator = SubjectScreeningFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_not_literate_witness_avail(self):
        self.options['is_literate'] = 'No'
        self.options['literate_witness_avail'] = 'No'
        form_validator = SubjectScreeningFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_minor_guardian_not_avail(self):
        self.options['is_minor'] = 'Yes'
        self.options['guardian_available'] = 'No'
        form_validator = SubjectScreeningFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, form_validator.validate)


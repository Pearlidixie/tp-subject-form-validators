from django.test import TestCase
from tp_screening.mommy_recipes import subjectscreening
from tp_screening.models import SubjectScreening
from tp_screening.constants import MALE
from model_mommy import mommy
from tp_subject_form_validators.form_validators import subject_screening
from tp_subject.constants import SINGLE


class TestDemographic(TestCase):

    def test_subject_screening(self):
        subject_screening = mommy.make_recipe(
            'tp_screening.subjectscreening')
        demographic = mommy.make_recipe(
            'tp_subject.demographic',
            marital_status=SINGLE,
            number_wives=None,
            number_husbands=None)
        self.assertTrue(subject_screening.gender, MALE)
        self.assertEqual(demographic.marital_status, SINGLE)
        self.assertIsNone(demographic.number_wives)
        self.assertIsNone(demographic.number_husbands)

    def test_subject_screening_t(self):
        subject_screening = mommy.make_recipe(
            'tp_screening.subjectscreening')
        demographic = mommy.make_recipe(
            'tp_subject.demographic',
            marital_status=SINGLE,
            number_wives=None,
            number_husbands=None)
        self.assertTrue(subject_screening.gender, MALE)
        self.assertEqual(demographic.marital_status, SINGLE)
        self.assertIsNone(demographic.number_wives)
        self.assertIsNone(demographic.number_husbands)

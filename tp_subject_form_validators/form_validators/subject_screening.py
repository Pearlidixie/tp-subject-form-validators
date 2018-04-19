from django.apps import apps as django_apps
from django import forms


class SubjectScreeningFormValidator():

    subject_screening_model = 'tp_screening.subjectscreening'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gender = self.cleaned_data.get('gender')
        self.is_citizen = self.cleaned_data.get('is_citizen')
        self.is_married_citizen = self.cleaned_data.get('is_married_citizen')
        self.marriage_proof = self.cleaned_data.get('marriage_proof')
        self.is_literate = self.cleaned_data.get('is_literate')
        self.literate_witness_avail = self.cleaned_data.get('literate_witness_avail')
        self.is_minor = self.cleaned_data.get('is_minor')
        self.guardian_available = self.cleaned_data.get('guardian_available')

    @property
    def subject_screening_model_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    def clean(self):

        if self.is_citizen == "No" and self.is_married_citizen == "No":
            raise forms.ValidationError('one has to be a citizen if not must be married to a Motswana and have documents')

        if self.is_citizen == "No" and self.is_married_citizen == "Yes":
            if self.marriage_proof == "No":
                raise forms.ValidationError('one has to be a citizen if not must be married to a Motswana and have documents')

        if self.is_literate == "No" and self.literate_witness_avail == "No":
            raise forms.ValidationError('Must be literate or have a witness available')

        if self.is_minor == "Yes" and self.guardian_available == "No":
            raise forms.ValidationError('Should not be a minor or have a guardian available')

 
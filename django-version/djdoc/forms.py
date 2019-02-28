from django.forms import ModelForm
from django import forms
from djversion.forms import VersionFormMixin

from djdoc.models import Document

# VersionFormMixin to overwrite fields 
class DocumentForm(VersionFormMixin,ModelForm):
    class Meta:
        model = Document
        exclude = ['created_by', 'modified_by','status']
        
    def clean(self):
        if not self.has_changed():
            raise forms.ValidationError('Document has not changed')
        return  self.cleaned_data    
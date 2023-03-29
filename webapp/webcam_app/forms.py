from django import forms
from .models import Counseling

class CounselingForm(forms.ModelForm):
    class Meta:
        model = Counseling
        fields = ['customername', 'counsel_subject', 'content', 'storage_data']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': '상담내역입력'}),
        }
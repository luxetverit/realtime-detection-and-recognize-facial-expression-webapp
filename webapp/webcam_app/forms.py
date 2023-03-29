from django import forms
from .models import Counseling

class CounselingForm(forms.ModelForm):
    class Meta:
        model = Counseling
        fields = ['userid', 'customername', 'counsel_subject', 'content', 'raw_data', 'stroage_data', 'legacy_data']
        widgets = {
            'counsel_subject' : forms.Textarea(attrs={'placeholder': '상담주제입력'}),
            'content': forms.Textarea(attrs={'placeholder': '상담내역입력'}),
        }
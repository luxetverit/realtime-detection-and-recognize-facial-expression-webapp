from django import forms
from .models import Counseling

class CounselingForm(forms.ModelForm):
    class Meta:
        model = Counseling

        fields = ['customername', 'counsel_subject', 'content', 'storage_data','realtime_true_false']


        widgets = {
            'customername': forms.TextInput(attrs={'placeholder': '고객 이름', 'class': 'form-control d-grid'}),
            'counsel_subject': forms.TextInput(attrs={'placeholder': '고객 이름', 'class': 'form-control d-grid'}),
            'content': forms.Textarea(attrs={'placeholder': '상담내역입력',}),
        }
        
class CounselingEditForm(forms.ModelForm):
    class Meta:
        model = Counseling

        fields = ['customername', 'counsel_subject', 'content', 'storage_data']
        exclude = ['realtime_true_false']

        widgets = {
            'customername': forms.TextInput(attrs={'placeholder': '고객 이름', 'class': 'form-control d-grid'}),
            'counsel_subject': forms.TextInput(attrs={'placeholder': '고객 이름', 'class': 'form-control d-grid'}),
            'content': forms.Textarea(attrs={'placeholder': '상담내역입력',}),
        }
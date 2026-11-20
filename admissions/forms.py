from django import forms
from .models import Admission
from courses.models import Course


class AdmissionForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(is_active=True),
        required=True,
        label='Select Course'
    )

    class Meta:
        model = Admission
        fields = ['first_name', 'last_name', 'email', 'phone', 'course', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

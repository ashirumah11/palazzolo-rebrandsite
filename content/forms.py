from django import forms
from .models import EventRegistration


class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control ptvti-input',
                'placeholder': 'Your Full Name',
                'required': 'required',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control ptvti-input',
                'placeholder': 'name@example.com',
                'required': 'required',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control ptvti-input',
                'placeholder': '+254 7XX XXX XXX',
            }),
        }
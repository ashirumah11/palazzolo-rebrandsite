from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('admissions', 'Admissions & Course Enquiries'),
        ('fees', 'Fee Structure & Payments'),
        ('attachments', 'Industrial Attachments & Partnerships'),
        ('general', 'General Institutional Inquiries'),
    ]

    enquiry_category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select ptvti-input', 'id': 'enquiry_category'})
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control ptvti-input',
                'placeholder': 'Your Full Name',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control ptvti-input',
                'placeholder': 'name@example.com',
                'required': 'required'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control ptvti-input',
                'placeholder': '+254 7XX XXX XXX',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control ptvti-input',
                'placeholder': 'Brief Subject of Your Inquiry',
                'required': 'required'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control ptvti-input',
                'rows': 5,
                'placeholder': 'How can we assist you? Tell us about your course interest or questions...',
                'required': 'required'
            }),
        }

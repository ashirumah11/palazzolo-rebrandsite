from django import forms
from .models import Admission
from courses.models import Course, Department


class AdmissionForm(forms.ModelForm):
    course_type = forms.ChoiceField(
        choices=[('', 'Select Course Type')] + Course.COURSE_TYPE_CHOICES,
        required=True,
        label='Course Type',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_course_type'})
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all().order_by('name'),
        required=False,
        label='Department',
        empty_label='Select Department',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_department'})
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        required=True,
        label='Select Course',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_course'})
    )

    class Meta:
        model = Admission
        fields = ['first_name', 'last_name', 'email', 'phone', 'course_type', 'department', 'course', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pre-filter courses based on initial data
        course_type = self.data.get('course_type') or self.initial.get('course_type')
        department_id = self.data.get('department') or self.initial.get('department')

        courses = Course.objects.filter(is_active=True)

        if course_type:
            courses = courses.filter(course_type=course_type)
        if department_id:
            courses = courses.filter(department_id=department_id)

        self.fields['course'].queryset = courses.order_by('department__name', 'specialization', 'title')

    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get('course')
        course_type = cleaned_data.get('course_type')
        department = cleaned_data.get('department')

        if course:
            if course_type and course.course_type != course_type:
                self.add_error('course', 'Selected course does not match the chosen course type.')
            if department and course.department != department:
                self.add_error('course', 'Selected course does not belong to the chosen department.')

        return cleaned_data

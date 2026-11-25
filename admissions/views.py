import random
import json
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics

from .forms import AdmissionForm
from .models import Admission, Fee
from .serializers import AdmissionSerializer, FeeSerializer
from courses.models import Course


class FeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Fee.objects.filter(is_published=True)
    serializer_class = FeeSerializer


class FeeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer


class AdmissionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer


class AdmissionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer


def admission_apply_view(request):
    if request.method == 'POST':
        form = AdmissionForm(request.POST)
        if form.is_valid():
            admission = form.save(commit=False)
            admission.status = 'pending'
            admission.save()
            ref = f"PTVTI-{admission.id:04d}-{random.randint(1000, 9999)}"
            messages.success(
                request,
                f"Application received. Your tracking reference is {ref}. Use it with your email to track status."
            )
            return redirect('admission_track')
    else:
        initial = {}
        course_id = request.GET.get('course')
        department_id = request.GET.get('department')
        course_type = request.GET.get('type')

        if course_id:
            initial['course'] = course_id
        if department_id:
            initial['department'] = department_id
        if course_type:
            initial['course_type'] = course_type

        form = AdmissionForm(initial=initial)

    return render(request, 'admissions/apply.html', {'form': form})


def admission_track_view(request):
    email = request.GET.get('email', '').strip()
    ref = request.GET.get('ref', '').strip()
    admission = None
    if email:
        try:
            admission = Admission.objects.filter(email=email).order_by('-applied_at').first()
        except Admission.DoesNotExist:
            admission = None

    return render(request, 'admissions/track.html', {
        'email': email,
        'ref': ref,
        'admission': admission,
    })


def course_options_view(request):
    """AJAX endpoint to fetch filtered course options."""
    department_id = request.GET.get('department')
    course_type = request.GET.get('course_type')

    courses = Course.objects.filter(is_active=True).select_related('department')

    if department_id:
        courses = courses.filter(department_id=department_id)
    if course_type:
        courses = courses.filter(course_type=course_type)

    courses = courses.order_by('specialization', 'title')

    data = list(courses.values(
        'id', 'title', 'slug', 'course_type', 'specialization', 'duration_months'
    ))

    return JsonResponse(data, safe=False)


def fees_list_view(request):
    """
    Public Fees Structure page displaying published course fees.
    Fees are grouped by department and course for easy reference.
    """
    departments = list(Fee.objects.filter(is_published=True)
                       .select_related('course__department')
                       .order_by('course__department__name', 'course__title')
                       .values_list('course__department', flat=True)
                       .distinct())

    department_fees = {}
    for dept_id in departments:
        if not dept_id:
            continue
        from courses.models import Department
        dept = Department.objects.filter(id=dept_id).first()
        if not dept:
            continue
        fees = Fee.objects.filter(
            is_published=True,
            course__department=dept
        ).select_related('course').order_by('course__title', 'fee_type')

        dept_fees_data = []
        for fee in fees:
            course_fees = next((d for d in dept_fees_data if d['course'] == fee.course), None)
            if course_fees:
                course_fees['fees'].append(fee)
            else:
                dept_fees_data.append({
                    'course': fee.course,
                    'fees': [fee]
                })
        department_fees[dept] = dept_fees_data

    context = {
        'department_fees': department_fees,
    }
    return render(request, 'admissions/fees_list.html', context)


def admission_requirements_view(request):
    """
    Admission Requirements - Coming Soon page.
    Displays a professional placeholder page for admission requirements
    that can be replaced with real content from a CMS in the future.
    """
    return render(request, 'admissions/requirements.html')


def admission_procedures_view(request):
    """
    Admission Procedures - Coming Soon page.
    Displays a professional placeholder page for admission procedures
    that can be replaced with real content from a CMS in the future.
    """
    return render(request, 'admissions/procedures.html')

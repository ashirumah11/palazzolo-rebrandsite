import random
import json
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics

from .forms import AdmissionForm
from .models import Admission
from .serializers import AdmissionSerializer
from courses.models import Course


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

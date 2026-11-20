from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from rest_framework import generics

from .models import Course, Department
from .serializers import CourseSerializer, DepartmentSerializer


class DepartmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


def course_list_view(request):
    query = request.GET.get('q', '').strip()
    dept_slug = request.GET.get('dept', '').strip()
    courses = Course.objects.filter(is_active=True).select_related('department')
    departments = Department.objects.all().order_by('name')

    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(department__name__icontains=query)
        )

    if dept_slug:
        courses = courses.filter(department__name__icontains=dept_slug)

    context = {
        'courses': courses,
        'departments': departments,
        'query': query,
    }
    return render(request, 'courses/course_list.html', context)


def course_detail_view(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    related = Course.objects.filter(
        department=course.department,
        is_active=True
    ).exclude(pk=course.pk)[:4]
    context = {
        'course': course,
        'related_courses': related,
    }
    return render(request, 'courses/course_detail.html', context)

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


def department_detail_view(request, slug):
    dept_name = slug.replace('-', ' ')
    departments = list(Department.objects.all())
    department = None
    for dept in departments:
        if dept.name.lower().replace(' ', '-') == slug.lower() or dept.name.lower() == dept_name.lower():
            department = dept
            break
    if not department:
        from django.http import Http404
        raise Http404("Department not found")
    courses = department.courses.filter(is_active=True)
    context = {
        'department': department,
        'courses': courses,
    }
    return render(request, 'departments/department_detail.html', context)

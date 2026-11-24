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
    from django.utils.text import slugify as django_slugify
    target = slug.lower().strip()
    target_clean = target.replace('-department', '').replace('_department', '').replace(' ', '-').strip('-')
    target_words = set(w for w in target.replace('-', ' ').replace('_', ' ').split() if w not in ('department', 'dept'))

    departments = list(Department.objects.all())
    department = None

    # 1. Exact slugify match
    for dept in departments:
        dept_slug = django_slugify(dept.name)
        if dept_slug == target or dept_slug == target_clean:
            department = dept
            break

    # 2. Match with '-department' stripped or appended
    if not department:
        for dept in departments:
            dept_slug = django_slugify(dept.name)
            dept_slug_clean = dept_slug.replace('-department', '').replace('_department', '').strip('-')
            if dept_slug_clean == target_clean or f"{dept_slug_clean}-department" == target:
                department = dept
                break

    # 3. Flexible substring or word overlap match (e.g. 'cosmetology' matches 'Cosmetology & Hairdressing')
    if not department:
        for dept in departments:
            dept_slug = django_slugify(dept.name)
            dept_slug_clean = dept_slug.replace('-department', '').replace('_department', '').strip('-')
            dept_words = set(w for w in dept.name.lower().replace('&', ' ').replace('-', ' ').split() if w not in ('department', 'dept'))
            if target_clean in dept_slug_clean or dept_slug_clean in target_clean or (target_words and target_words.intersection(dept_words)):
                department = dept
                break

    # 4. Fallback: match by ID if numeric
    if not department and target.isdigit():
        department = next((d for d in departments if str(d.id) == target), None)

    if not department:
        from django.http import Http404
        raise Http404("Department not found")

    courses = department.courses.filter(is_active=True)
    context = {
        'department': department,
        'courses': courses,
    }
    return render(request, 'departments/department_detail.html', context)

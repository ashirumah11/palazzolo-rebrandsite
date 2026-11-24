from django.test import TestCase
from django.urls import reverse
from .models import Course, Department


class CourseViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        dept = Department.objects.create(name='Test Dept')
        Course.objects.create(title='Test Course', slug='test-course', department=dept, is_active=True)

    def test_course_list(self):
        resp = self.client.get(reverse('course_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Course')

    def test_department_detail_slug_variations(self):
        dept = Department.objects.filter(name='Cosmetology & Hairdressing').first()
        if not dept:
            dept = Department.objects.create(name='Cosmetology & Hairdressing')
        Course.objects.update_or_create(slug='hair-styling', defaults={'title': 'Hair Styling', 'department': dept, 'is_active': True})

        for slug in ['cosmetology-hairdressing-department', 'cosmetology-hairdressing', 'cosmetology', 'hairdressing']:
            resp = self.client.get(f'/departments/{slug}/')
            self.assertEqual(resp.status_code, 200, f"Failed on slug: {slug}")
            self.assertContains(resp, 'Hair Styling')


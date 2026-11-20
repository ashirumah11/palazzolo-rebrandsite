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

    def test_course_detail(self):
        resp = self.client.get(reverse('course_detail', args=['test-course']))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Test Course')


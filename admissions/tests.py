from django.test import TestCase
from django.urls import reverse
from courses.models import Course, Department


class AdmissionViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        dept = Department.objects.create(name='Dept')
        cls.course = Course.objects.create(title='Course', slug='course', department=dept, is_active=True)

    def test_apply_get(self):
        resp = self.client.get(reverse('admission_apply'))
        self.assertEqual(resp.status_code, 200)

    def test_apply_post(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '0712345678',
            'course': self.course.id,
            'message': 'Apply'
        }
        resp = self.client.post(reverse('admission_apply'), data, follow=True)
        self.assertEqual(resp.status_code, 200)


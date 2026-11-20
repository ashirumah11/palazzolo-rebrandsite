from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import ContactMessage, DepartmentContact


class ContactsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='securepassword123',
            is_staff=True,
        )
        self.dept_contact = DepartmentContact.objects.create(
            department='ICT Department',
            phone='+254700000000',
            email='ict@palazzolotechnical.co.ke',
            address='Kihara-Gachie, Kiambu',
        )

    def test_submit_contact_message(self):
        payload = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': '+254711223344',
            'subject': 'Admissions Enquiry',
            'message': 'I would like to inquire about ICT certificate courses.',
        }
        url = reverse('contactmessage-list-create')
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.first().name, 'Jane Doe')

    def test_list_contact_messages_requires_auth(self):
        url = reverse('contactmessage-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_contact_messages_authenticated(self):
        ContactMessage.objects.create(
            name='John Smith',
            email='john@example.com',
            subject='Fee query',
            message='What are the fees for Electrical Engineering?',
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('contactmessage-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_department_contacts_list_public(self):
        url = reverse('departmentcontact-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['department'], 'ICT Department')

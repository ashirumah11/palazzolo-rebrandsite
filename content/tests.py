from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from .models import (
    Announcement,
    HeroCarouselItem,
    StaffMember,
    EventItem,
    Testimonial,
    GalleryItem,
    EventRegistration,
)
from news.models import NewsArticle


class ContentApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='secure-pass-123',
            is_staff=True,
        )
        Announcement.objects.create(title='Launch', message='Announcement', is_active=True)
        StaffMember.objects.create(name='Alice', role='Director', is_active=True)
        EventItem.objects.create(title='Open Day', starts_at='2026-08-01T09:00:00Z', is_active=True)
        Testimonial.objects.create(author='Bob', quote='Great school', is_active=True)
        GalleryItem.objects.create(title='Campus', image='gallery/campus.jpg', is_active=True)
        HeroCarouselItem.objects.create(
            title='Learn by doing',
            subtitle='Build practical skills that matter.',
            image='gallery/hero-slide.jpg',
            is_active=True,
            order=1,
        )

    def test_announcements_list(self):
        url = reverse('announcement-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_staff_list(self):
        url = reverse('staffmember-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_events_list(self):
        url = reverse('eventitem-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_testimonials_list(self):
        url = reverse('testimonial-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_gallery_list(self):
        url = reverse('galleryitem-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_hero_carousel_list(self):
        url = reverse('herocarouselitem-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_hero_carousel_create(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('herocarouselitem-list-create')

        image_bytes = BytesIO()
        Image.new('RGB', (10, 10), color='blue').save(image_bytes, format='PNG')
        image_bytes.seek(0)

        payload = {
            'title': 'Industry-ready training',
            'subtitle': 'Practical learning with modern facilities.',
            'image': SimpleUploadedFile('hero.png', image_bytes.read(), content_type='image/png'),
            'button_text': 'Apply now',
            'button_link': '/courses/',
            'is_active': True,
            'order': 2,
        }
        response = self.client.post(url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HeroCarouselItem.objects.count(), 2)

    def test_hero_carousel_relative_and_absolute_links(self):
        from django.core.exceptions import ValidationError

        # Relative path like /courses/ must be valid
        item_relative = HeroCarouselItem(title='Courses', button_link='/courses/')
        item_relative.full_clean()
        item_relative.save()

        # Absolute URL must be valid
        item_absolute = HeroCarouselItem(title='Portal', button_link='https://example.com/portal')
        item_absolute.full_clean()
        item_absolute.save()

        # Anchor link must be valid
        item_anchor = HeroCarouselItem(title='Contact', button_link='#contact')
        item_anchor.full_clean()
        item_anchor.save()

        # Invalid URL must raise ValidationError
        item_invalid = HeroCarouselItem(title='Broken', button_link='htp://broken url')
        with self.assertRaises(ValidationError):
            item_invalid.full_clean()


class PublicPagesViewTests(TestCase):
    def setUp(self):
        from courses.models import Department, Course
        self.dept = Department.objects.create(name='Engineering Department', description='Practical trades')
        self.course = Course.objects.create(
            title='Electrical Installation',
            slug='electrical-installation',
            department=self.dept,
            duration_months=12,
            is_active=True
        )

    def test_homepage_renders_successfully(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PALAZZOLO')
        self.assertContains(response, 'Electrical Installation')
        self.assertContains(response, 'TVETA Accredited')

    def test_about_page_renders_successfully(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Poverelle Sisters')
        self.assertContains(response, 'Born from Hope, Built for Transformation')
        self.assertContains(response, 'Respect')
        self.assertContains(response, 'Integrity')

    def test_contact_page_get(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Send Us a Message')
        self.assertContains(response, 'Campus Contact Info')

    def test_contact_form_submission(self):
        from contacts.models import ContactMessage
        payload = {
            'name': 'Francis Kariuki',
            'email': 'francis@example.com',
            'phone': '+254722123456',
            'enquiry_category': 'admissions',
            'subject': 'Intake dates for Electrical Engineering',
            'message': 'When does the May intake start for certificate classes?',
        }
        response = self.client.post('/contact/', payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactMessage.objects.filter(email='francis@example.com').exists())
        self.assertContains(response, 'PTVTI-MSG-')

    def test_news_list_page_renders(self):
        NewsArticle.objects.create(
            title='Test News',
            slug='test-news',
            summary='Test summary',
            content='Test content',
            is_published=True,
        )
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test News')

    def test_news_detail_page_renders(self):
        article = NewsArticle.objects.create(
            title='Detail News',
            slug='detail-news',
            summary='Detail summary',
            content='Detail content',
            is_published=True,
        )
        response = self.client.get(f'/news/{article.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detail News')

    def test_event_list_page_renders(self):
        EventItem.objects.create(
            title='Future Event',
            starts_at='2030-01-01T10:00:00Z',
            is_active=True,
        )
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Future Event')

    def test_event_detail_page_renders(self):
        event = EventItem.objects.create(
            title='Detail Event',
            starts_at='2030-01-01T10:00:00Z',
            is_active=True,
        )
        response = self.client.get(f'/events/{event.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detail Event')

    def test_event_registration_success(self):
        event = EventItem.objects.create(
            title='Registerable Event',
            starts_at='2030-01-01T10:00:00Z',
            is_active=True,
        )
        payload = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+254700000000',
        }
        response = self.client.post(f'/events/{event.pk}/', payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(EventRegistration.objects.filter(email='test@example.com', event=event).exists())
        self.assertContains(response, 'Thank you')

    def test_event_registration_duplicate_prevented(self):
        event = EventItem.objects.create(
            title='Duplicate Event',
            starts_at='2030-01-01T10:00:00Z',
            is_active=True,
        )
        EventRegistration.objects.create(event=event, name='Existing', email='existing@example.com')
        payload = {
            'name': 'New User',
            'email': 'existing@example.com',
            'phone': '+254700000001',
        }
        response = self.client.post(f'/events/{event.pk}/', payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already registered')

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Announcement, StaffMember, EventItem, Testimonial, GalleryItem, HeroCarouselItem
from courses.models import Department, Course
from news.models import NewsArticle
from .serializers import (
    AnnouncementSerializer,
    StaffMemberSerializer,
    EventItemSerializer,
    TestimonialSerializer,
    GalleryItemSerializer,
    HeroCarouselItemSerializer,
)


def home_view(request):
    """
    Public Homepage rendering dynamic hero slides, value pillars,
    featured departments & courses, verified stats, news, events, and testimonials.
    """
    hero_slides = HeroCarouselItem.objects.filter(is_active=True).order_by('order', '-created_at')
    departments = Department.objects.all().prefetch_related('courses')
    featured_courses = Course.objects.filter(is_active=True).select_related('department')[:6]
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order', '-created_at')[:4]
    upcoming_events = EventItem.objects.filter(is_active=True).order_by('starts_at')[:3]
    latest_news = NewsArticle.objects.filter(is_published=True).order_by('-published_at')[:3]
    gallery_preview = GalleryItem.objects.filter(is_active=True).order_by('order')[:6]

    context = {
        'hero_slides': hero_slides,
        'departments': departments,
        'featured_courses': featured_courses,
        'testimonials': testimonials,
        'upcoming_events': upcoming_events,
        'latest_news': latest_news,
        'gallery_preview': gallery_preview,
    }
    return render(request, 'pages/home.html', context)


def about_view(request):
    """
    Public About PTVTI page detailing institutional history (Poverelle Sisters),
    mission, vision, core values, facilities, and leadership.
    """
    staff_members = StaffMember.objects.filter(is_active=True).order_by('display_order', 'name')
    departments = Department.objects.all().order_by('name')
    gallery_items = GalleryItem.objects.filter(is_active=True).order_by('order')[:8]

    context = {
        'staff_members': staff_members,
        'departments': departments,
        'gallery_items': gallery_items,
    }
    return render(request, 'pages/about.html', context)


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Announcement.objects.all()
        if self.action == 'list':
            return queryset.filter(is_active=True)
        return queryset

class StaffMemberViewSet(viewsets.ModelViewSet):
    queryset = StaffMember.objects.all()
    serializer_class = StaffMemberSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class EventItemViewSet(viewsets.ModelViewSet):
    queryset = EventItem.objects.all()
    serializer_class = EventItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = EventItem.objects.all()
        if self.action == 'list':
            return queryset.filter(is_active=True)
        return queryset

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class GalleryItemViewSet(viewsets.ModelViewSet):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = GalleryItem.objects.all()
        if self.action == 'list':
            return queryset.filter(is_active=True)
        return queryset


class HeroCarouselItemViewSet(viewsets.ModelViewSet):
    queryset = HeroCarouselItem.objects.all()
    serializer_class = HeroCarouselItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = HeroCarouselItem.objects.all()
        if self.action == 'list':
            return queryset.filter(is_active=True)
        return queryset
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone
from django.db import IntegrityError, transaction
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Announcement, StaffMember, EventItem, Testimonial, GalleryItem, HeroCarouselItem, EventRegistration
from .forms import EventRegistrationForm
from courses.models import Department, Course
from news.models import NewsArticle
from .serializers import (
    AnnouncementSerializer,
    StaffMemberSerializer,
    EventItemSerializer,
    TestimonialSerializer,
    GalleryItemSerializer,
    HeroCarouselItemSerializer,
    EventRegistrationSerializer,
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


def event_list_view(request):
    """
    Public Events Hub with upcoming vs. past filtering.
    """
    now = timezone.now()
    upcoming = request.GET.get('filter', 'upcoming') == 'upcoming'
    queryset = EventItem.objects.filter(is_active=True).select_related()
    if upcoming:
        queryset = queryset.filter(starts_at__gte=now).order_by('starts_at')
    else:
        queryset = queryset.filter(starts_at__lt=now).order_by('-starts_at')

    context = {
        'events': queryset,
        'is_upcoming': upcoming,
        'now': now,
    }
    return render(request, 'content/event_list.html', context)


def event_detail_view(request, pk):
    """
    Public event detail page with registration form and attendee count.
    """
    event = get_object_or_404(EventItem, pk=pk, is_active=True)
    now = timezone.now()
    registrations = EventRegistration.objects.filter(event=event).select_related()

    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            try:
                with transaction.atomic():
                    registration.save()
                messages.success(
                    request,
                    f"Thank you, {registration.name}! You are registered for '{event.title}'."
                )
                return redirect('event_detail', pk=pk)
            except IntegrityError:
                messages.error(
                    request,
                    "You are already registered for this event with this email address."
                )
    else:
        form = EventRegistrationForm()

    context = {
        'event': event,
        'form': form,
        'registrations': registrations,
        'now': now,
        'registration_count': registrations.count(),
    }
    return render(request, 'content/event_detail.html', context)


def gallery_list_view(request):
    """
    Public Gallery Hub with category filtering and YouTube video support.
    Items can be images or YouTube videos with category filtering.
    """
    categories = GalleryItem.CATEGORY_CHOICES
    selected_category = request.GET.get('category', '')

    queryset = GalleryItem.objects.filter(is_active=True).prefetch_related()

    if selected_category:
        queryset = queryset.filter(category=selected_category)

    gallery_items = queryset.order_by('order', '-created_at')

    context = {
        'gallery_items': gallery_items,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'content/gallery_list.html', context)


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


class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all().select_related('event')
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = EventRegistration.objects.all().select_related('event')
        if self.action == 'list':
            return queryset
        return queryset
import re

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models


def extract_youtube_id(url):
    """
    Extract YouTube video ID from various YouTube URL formats.
    Returns None if not a valid YouTube URL.
    """
    if not url:
        return None

    youtube_regex = (
        r'(?:https?://)?'
        r'(?:www\.)?'
        r'(?:youtube\.com|youtu\.be)'
        r'(?:/watch\?v=|/v/|/(?:embed|e)/|youtu\.be/|#video/)'
        r'([0-9A-Za-z_-]{11})'
    )

    match = re.search(youtube_regex, str(url))
    return match.group(1) if match else None


def validate_web_link(value):
    """
    Validates that a URL is either:
    1. A relative internal path, anchor, or protocol (e.g., '/courses/', '#contact', 'tel:+254...', 'mailto:info@...')
    2. A valid absolute URL with scheme (e.g., 'https://...', 'http://...')
    """
    if not value:
        return
    trimmed = str(value).strip()
    if trimmed.startswith(('/', '#', '?', 'tel:', 'mailto:')):
        return
    validator = URLValidator()
    validator(trimmed)


class Announcement(models.Model):
    title = models.CharField(max_length=220)
    message = models.TextField()
    link = models.CharField(
        max_length=500,
        blank=True,
        validators=[validate_web_link],
        help_text="Internal path (e.g. /admissions/apply/) or full URL (e.g. https://...)."
    )
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = 'Announcements'

    def __str__(self):
        return self.title


class StaffMember(models.Model):
    name = models.CharField(max_length=160)
    role = models.CharField(max_length=160)
    department = models.CharField(max_length=160, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='staff/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class EventItem(models.Model):
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=220, blank=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-starts_at']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    author = models.CharField(max_length=160)
    role = models.CharField(max_length=160, blank=True)
    quote = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.author

class GalleryItem(models.Model):
    """
    Gallery item supporting both images and YouTube videos.
    Category choices for filtering: events, facilities, courses, student-life, achievements.
    """
    CATEGORY_CHOICES = [
        ('events', 'Events'),
        ('facilities', 'Facilities'),
        ('courses', 'Courses'),
        ('student-life', 'Student Life'),
        ('achievements', 'Achievements'),
        ('other', 'Other'),
    ]

    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'YouTube Video'),
    ]

    title = models.CharField(max_length=220)
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    video_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="YouTube video URL (e.g., https://www.youtube.com/watch?v=...)"
    )
    caption = models.CharField(max_length=320, blank=True)
    alt_text = models.CharField(max_length=220, blank=True)
    category = models.CharField(max_length=120, choices=CATEGORY_CHOICES, blank=True, default='other')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    @property
    def media_type(self):
        """Return the media type for display purposes."""
        if self.image:
            return 'image'
        if self.video_url:
            return 'video'
        return None

    @property
    def youtube_video_id(self):
        """Extract and return the YouTube video ID from the URL."""
        return extract_youtube_id(self.video_url)

    @property
    def is_youtube_video(self):
        """Check if this item has a valid YouTube video."""
        return bool(self.youtube_video_id)

    def clean(self):
        """Validate that only one of image or video_url is provided."""
        from django.core.exceptions import ValidationError
        if self.image and self.video_url:
            raise ValidationError('An item cannot have both an image and a video URL. Choose one or the other.')
        if not self.image and not self.video_url:
            raise ValidationError('An item must have either an image or a video URL.')

    def get_embed_url(self):
        """Return the YouTube embed URL for video items."""
        if self.is_youtube_video:
            return f'https://www.youtube.com/embed/{self.youtube_video_id}'
        return None


class HeroCarouselItem(models.Model):
    title = models.CharField(max_length=220)
    subtitle = models.TextField(blank=True)
    image = models.ImageField(upload_to='hero-carousel/', blank=True, null=True)
    button_text = models.CharField(max_length=80, blank=True)
    button_link = models.CharField(
        max_length=500,
        blank=True,
        validators=[validate_web_link],
        help_text="Internal path (e.g. /courses/) or full URL (e.g. https://...)."
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Hero Carousel Item'
        verbose_name_plural = 'Hero Carousel Items'

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    """
    Public registration for an institutional event.
    A unique email may register only once per event to prevent duplicates.
    """
    event = models.ForeignKey(
        EventItem,
        related_name='registrations',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-registered_at']
        unique_together = ('event', 'email')
        verbose_name = 'Event Registration'
        verbose_name_plural = 'Event Registrations'

    def __str__(self):
        return f'{self.name} - {self.event.title}'
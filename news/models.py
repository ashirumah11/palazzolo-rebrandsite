from django.db import models


class NewsArticle(models.Model):
    CATEGORY_CHOICES = [
        ('Announcements', 'Announcements'),
        ('Events', 'Events'),
        ('Achievements', 'Achievements'),
        ('General', 'General'),
    ]

    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True)
    summary = models.CharField(max_length=320)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    author = models.CharField(max_length=120, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General', help_text="Category for filtering news articles")
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

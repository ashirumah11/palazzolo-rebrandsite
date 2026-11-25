from django.db import models
from courses.models import Course
from django.core.validators import MinValueValidator


class Fee(models.Model):
    """
    Course-specific fees for PTVTI programs.
    Admins can set and publish fees for individual courses.
    """
    FEE_TYPE_CHOICES = [
        ('application', 'Application Fee'),
        ('tuition', 'Tuition Fee'),
        ('registration', 'Registration Fee'),
        ('other', 'Other'),
    ]

    course = models.ForeignKey(
        Course,
        related_name='fees',
        on_delete=models.CASCADE,
        help_text='The course this fee applies to'
    )
    fee_type = models.CharField(
        max_length=20,
        choices=FEE_TYPE_CHOICES,
        default='tuition',
        help_text='Type of fee'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Fee amount in Kenyan Shillings'
    )
    is_published = models.BooleanField(
        default=True,
        help_text='Show this fee on the Fees Structure page'
    )
    note = models.TextField(
        blank=True,
        help_text='Additional notes or description for this fee'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course__department', 'course__title', 'fee_type']
        unique_together = ['course', 'fee_type']

    def __str__(self):
        return f'{self.get_fee_type_display()}: {self.course.title} - KSh {self.amount}'

    @property
    def formatted_amount(self):
        """Return amount formatted with KSh and comma separators."""
        return f"KSh {self.amount:,.0f}"


class Admission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=24)
    course = models.ForeignKey(
        Course,
        related_name='admissions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)

    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

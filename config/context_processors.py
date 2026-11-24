import calendar
from datetime import timedelta

from admissions.models import Admission
from contacts.models import ContactMessage, DepartmentContact
from content.models import Announcement, EventItem, GalleryItem, StaffMember, Testimonial
from courses.models import Course, Department
from django.utils import timezone
from news.models import NewsArticle


def _month_start(year, month):
    if month == 1:
        return year - 1, 12
    return year, month - 1


def admin_dashboard(request):
    if not request.path.startswith('/admin/'):
        return {}

    current_month = timezone.localdate().replace(day=1)
    trend_months = []
    year, month = current_month.year, current_month.month
    for _ in range(6):
        count = Admission.objects.filter(
            applied_at__year=year,
            applied_at__month=month,
        ).count()
        trend_months.append({'label': current_month.strftime('%b'), 'count': count})
        year, month = _month_start(year, month)
        current_month = current_month.replace(year=year, month=month)
    trend_months.reverse()
    trend_max = max((month['count'] for month in trend_months), default=0) or 1
    for month in trend_months:
        month['height'] = max(8, round(month['count'] / trend_max * 100))

    today = timezone.localdate()
    month_events = EventItem.objects.filter(
        is_active=True,
        starts_at__year=today.year,
        starts_at__month=today.month,
    ).order_by('starts_at')
    events_by_day = {}
    for event in month_events:
        events_by_day.setdefault(event.starts_at.astimezone(timezone.get_current_timezone()).day, []).append(event.title)
    calendar_weeks = [
        [
            {'day': day, 'events': events_by_day.get(day, [])} if day else {'day': '', 'events': []}
            for day in week
        ]
        for week in calendar.monthcalendar(today.year, today.month)
    ]
    recent_cutoff = timezone.now() - timedelta(days=30)
    notification_items = [
        {
            'label': 'New admissions',
            'count': Admission.objects.filter(applied_at__date=today).count(),
            'url': 'admin:admissions_admission_changelist',
        },
        {
            'label': 'New contact messages',
            'count': ContactMessage.objects.filter(status='new').count(),
            'url': 'admin:contacts_contactmessage_changelist',
        },
        {
            'label': 'New testimonials',
            'count': Testimonial.objects.filter(created_at__gte=recent_cutoff).count(),
            'url': 'admin:content_testimonial_changelist',
        },
        {
            'label': 'Gallery updated',
            'count': GalleryItem.objects.filter(updated_at__gte=recent_cutoff).count(),
            'url': 'admin:content_galleryitem_changelist',
        },
    ]

    return {
        'dashboard_notifications': notification_items,
        'calendar_month': today.strftime('%B %Y'),
        'calendar_weekdays': ('M', 'T', 'W', 'T', 'F', 'S', 'S'),
        'calendar_weeks': calendar_weeks,
        'dashboard_today': timezone.localdate(),
        'dashboard_stats': {
            'students': Admission.objects.filter(status='accepted').count(),
            'new_applications': Admission.objects.filter(applied_at__date=timezone.localdate()).count(),
            'pending_admissions': Admission.objects.filter(status='pending').count(),
            'accepted_admissions': Admission.objects.filter(status='accepted').count(),
            'rejected_admissions': Admission.objects.filter(status='rejected').count(),
            'total_admissions': Admission.objects.count(),
            'courses': Course.objects.filter(is_active=True).count(),
            'departments': Department.objects.count(),
            'unread_messages': ContactMessage.objects.filter(status='new').count(),
            'total_messages': ContactMessage.objects.count(),
            'news': NewsArticle.objects.filter(is_published=True).count(),
            'announcements': Announcement.objects.filter(is_active=True).count(),
            'upcoming_events': EventItem.objects.filter(is_active=True).count(),
            'staff': StaffMember.objects.filter(is_active=True).count(),
            'department_contacts': DepartmentContact.objects.count(),
            'gallery': GalleryItem.objects.filter(is_active=True).count(),
            'testimonials': Testimonial.objects.filter(is_active=True).count(),
        },
        'admissions_trend': trend_months,
        'recent_admissions': Admission.objects.select_related('course')[:5],
        'recent_messages': ContactMessage.objects.all()[:5],
        'upcoming_events_list': EventItem.objects.filter(is_active=True).order_by('starts_at')[:5],
    }


def ptvti_public_context(request):
    """
    Global context processor providing institutional identity, active announcements,
    and department taxonomy across all public Django templates.
    """
    if request.path.startswith('/admin/'):
        return {}

    try:
        active_announcement = Announcement.objects.filter(is_active=True).order_by('order', '-created_at').first()
    except Exception:
        active_announcement = None

    try:
        nav_departments = Department.objects.all().order_by('name')
    except Exception:
        nav_departments = []

    return {
        'ptvti_active_announcement': active_announcement,
        'ptvti_nav_departments': nav_departments,
        'ptvti_institution': {
            'name': 'Palazzolo Technical & Vocational Training Institute',
            'short_name': 'PTVTI',
            'motto': 'With God at the Centre, we serve, train and transform',
            'tagline': 'Learn. Innovate. Build Your Future.',
            'phone': '+254 700 000 000',
            'email': 'info@palazzolotechnical.co.ke',
            'admissions_email': 'admissions@palazzolotechnical.co.ke',
            'address': 'Off Kihara-Gachie-Karura Road, Kiambu County, Kenya',
            'postal_address': 'P.O. Box 1234 - 00200 Nairobi, Kenya',
            'accreditation': 'Accredited by TVETA Kenya | Affiliated with NITA & UNESCO',
            'location': {
                'latitude': -1.223992,
                'longitude': 36.7720694,
                'google_maps_url': 'https://www.google.com/maps?q=-1.223992,36.7720694&z=17&output=embed',
                'directions_url': 'https://www.google.com/maps/dir/?api=1&destination=-1.223992%2C36.7720694',
            },
            'physical_location': 'Gachie, Kiambu County, Kenya',
        },
        'ptvti_verified_stats': [
            {'value': 250, 'prefix': '', 'suffix': '+', 'label': 'Enrolled Students', 'icon': 'fas fa-user-graduate'},
            {'value': 150, 'prefix': '', 'suffix': '+', 'label': 'Graduated Alumni', 'icon': 'fas fa-graduation-cap'},
            {'value': 10, 'prefix': '', 'suffix': '+', 'label': 'Skills Awards Won', 'icon': 'fas fa-award'},
            {'value': 86, 'prefix': '', 'suffix': '%', 'label': 'Graduation & Placement Rate', 'icon': 'fas fa-chart-line'},
        ],
    }

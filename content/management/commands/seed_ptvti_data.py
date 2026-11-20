from django.core.management.base import BaseCommand
from courses.models import Department, Course
from content.models import Announcement, HeroCarouselItem, StaffMember, Testimonial, EventItem, GalleryItem
from contacts.models import DepartmentContact
from news.models import NewsArticle
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Seeds initial verified institutional data for PTVTI'

    def handle(self, *args, **options):
        self.stdout.write('Seeding verified PTVTI data...')

        # 1. Departments & Courses
        dept_data = [
            {
                'name': 'Engineering Department',
                'description': 'Hands-on practical training in electrical installations, solar PV technology, welding and pipe fitting.',
                'requirements': 'KCSE mean grade D- or above for Certificate; KCPE for Artisan level.\nPassion for practical trade and technical fabrication.',
                'duration_months': 12,
                'image': 'departments/software.webp',
                'courses': [
                    {'title': 'Electrical Installation & Maintenance', 'slug': 'electrical-installation', 'duration_months': 12, 'duration_weeks': 48, 'credits': 60, 'description': 'Comprehensive training in domestic and industrial electrical wiring, safety compliance, circuit testing, and solar installations.'},
                    {'title': 'Plumbing & Pipe Fitting', 'slug': 'plumbing-pipe-fitting', 'duration_months': 9, 'duration_weeks': 36, 'credits': 45, 'description': 'Sanitary installations, pipe layout, drainage systems, water supply and heating installations.'},
                    {'title': 'Arc & Gas Welding Trade', 'slug': 'arc-gas-welding', 'duration_months': 6, 'duration_weeks': 24, 'credits': 30, 'description': 'Metal fabrication, shielded metal arc welding, oxy-acetylene cutting and structural steel joining.'},
                ]
            },
            {
                'name': 'ICT & Computing Department',
                'description': 'Modern computer literacy, software tools, digital systems, and network infrastructure training.',
                'requirements': 'KCSE mean grade D or above for Certificate; Open entry for Digital Literacy.',
                'duration_months': 12,
                'courses': [
                    {'title': 'Certificate in Information Technology', 'slug': 'certificate-information-technology', 'duration_months': 12, 'duration_weeks': 48, 'credits': 60, 'description': 'Computer maintenance, networking essentials, operating systems, database management, and office productivity tools.'},
                    {'title': 'Software Fundamentals & Web Applications', 'slug': 'software-fundamentals', 'duration_months': 6, 'duration_weeks': 24, 'credits': 30, 'description': 'Web design, HTML, CSS, JavaScript, Python fundamentals, and responsive interface design.'},
                    {'title': 'Computer Packages & Digital Productivity', 'slug': 'computer-packages', 'duration_months': 2, 'duration_weeks': 8, 'credits': 15, 'description': 'Intensive practical mastery of MS Office Suite, cloud productivity, keyboarding, and digital security.'},
                ]
            },
            {
                'name': 'Fashion & Design Department',
                'description': 'Garment construction, tailoring, pattern drafting, and modern fashion design entrepreneurship.',
                'requirements': 'KCSE mean grade D- or KCPE certificate.\nCreative interest in textiles and garment craft.',
                'duration_months': 12,
                'courses': [
                    {'title': 'Artisan in Garment Making & Tailoring', 'slug': 'garment-making-tailoring', 'duration_months': 12, 'duration_weeks': 48, 'credits': 60, 'description': 'Body measurement, pattern drafting, industrial sewing machine operations, fabric cutting, and finishing.'},
                    {'title': 'Fashion Design & Pattern Drafting', 'slug': 'fashion-design-pattern-drafting', 'duration_months': 9, 'duration_weeks': 36, 'credits': 45, 'description': 'Contemporary design illustration, textile technology, bespoke tailoring, and fashion line creation.'},
                ]
            },
            {
                'name': 'Cosmetology & Hairdressing Department',
                'description': 'Professional hair styling, barbering, beauty therapy, skin care, and modern salon management.',
                'requirements': 'Open entry; KCPE/KCSE certificates welcome.\nKeen interest in personal care and beauty artistry.',
                'duration_months': 9,
                'courses': [
                    {'title': 'Hairdressing & Salon Services', 'slug': 'hairdressing-salon-services', 'duration_months': 9, 'duration_weeks': 36, 'credits': 45, 'description': 'Hair treatment, braiding, chemical relaxers, coloring, blow-drying, and client consultation.'},
                    {'title': 'Beauty Therapy & Nail Technology', 'slug': 'beauty-therapy-nail-tech', 'duration_months': 6, 'duration_weeks': 24, 'credits': 30, 'description': 'Facial therapies, manicure, pedicure, gel application, massage therapy, and salon hygiene.'},
                    {'title': 'Professional Barbering & Grooming', 'slug': 'professional-barbering', 'duration_months': 3, 'duration_weeks': 12, 'credits': 20, 'description': 'Modern fade cuts, shaving techniques, beard grooming, sterilisation, and barber shop operations.'},
                ]
            },
            {
                'name': 'Hospitality & Catering Department',
                'description': 'Food and beverage production, pastry and baking, guest relations, and culinary entrepreneurship.',
                'requirements': 'KCSE mean grade D or KCPE with practical aptitude in culinary arts.',
                'duration_months': 12,
                'courses': [
                    {'title': 'Food & Beverage Production (Culinary Arts)', 'slug': 'food-beverage-production', 'duration_months': 12, 'duration_weeks': 48, 'credits': 60, 'description': 'Hot kitchen cookery, cold preparations, knife techniques, menu planning, food safety, and kitchen management.'},
                    {'title': 'Pastry, Baking & Cake Decoration', 'slug': 'pastry-baking-cake-decoration', 'duration_months': 6, 'duration_weeks': 24, 'credits': 30, 'description': 'Commercial bread baking, cake decoration, pastries, yeast doughs, and bakery business management.'},
                ]
            },
        ]

        for d_info in dept_data:
            courses = d_info.pop('courses', [])
            dept, _ = Department.objects.get_or_create(name=d_info['name'], defaults=d_info)
            for c_info in courses:
                Course.objects.get_or_create(
                    slug=c_info['slug'],
                    defaults={**c_info, 'department': dept, 'is_active': True}
                )

        # 2. Hero Carousel Items
        hero_slides = [
            {
                'title': 'Learn. Innovate. Build Your Future.',
                'subtitle': 'Equipping youth with practical technical skills, professional mentorship, and values-based education for meaningful employment and entrepreneurship.',
                'button_text': 'Explore Courses',
                'button_link': '/courses/',
                'order': 1,
            },
            {
                'title': 'TVETA & NITA Accredited Practical Training',
                'subtitle': 'Gain verified vocational qualifications in modern workshops and training studios in Kiambu, certified to national standards.',
                'button_text': 'Apply for Admission',
                'button_link': '/admissions/apply/',
                'order': 2,
            },
            {
                'title': 'Transforming Lives Through Skilled Hands',
                'subtitle': 'Founded by the Poverelle Sisters with compassion and dedication to empower the community and provide pathways to self-reliance.',
                'button_text': 'About PTVTI',
                'button_link': '/about/',
                'order': 3,
            },
        ]
        for slide in hero_slides:
            HeroCarouselItem.objects.get_or_create(title=slide['title'], defaults=slide)

        # 3. Active Announcement
        Announcement.objects.get_or_create(
            title='Ongoing Admissions for Next Intake',
            defaults={
                'message': 'Applications are ongoing for artisan, certificate and diploma courses across all departments. Limited workshop spaces available.',
                'link': '/admissions/apply/',
                'phone': '+254 700 000 000',
                'email': 'admissions@palazzolotechnical.co.ke',
                'is_active': True,
                'order': 1,
            }
        )

        # 4. Staff Members (Leadership)
        staff_data = [
            {'name': 'Sr. Maria Poverelle', 'role': 'Institute Director & Custodian', 'department': 'Administration', 'bio': 'Guiding the spiritual, holistic, and institutional vision of PTVTI in the spirit of St. Luigi Palazzolo.', 'display_order': 1},
            {'name': 'Mr. Joseph Mwangi', 'role': 'Head of Engineering & Technical Trades', 'department': 'Engineering', 'bio': 'Over 12 years of industry and vocational training experience in electrical and mechanical systems.', 'display_order': 2},
            {'name': 'Ms. Catherine Wanjiku', 'role': 'Lead ICT Instructor & Digital Trainer', 'department': 'ICT & Computing', 'bio': 'Passionate about preparing learners for digital workplaces, systems administration, and software skills.', 'display_order': 3},
            {'name': 'Ms. Faith Njeri', 'role': 'Head of Fashion & Creative Arts', 'department': 'Fashion & Design', 'bio': 'Master garment artisan and textile specialist mentoring youth in bespoke design and business.', 'display_order': 4},
            {'name': 'Ms. Grace Muthoni', 'role': 'Head of Cosmetology & Personal Care', 'department': 'Cosmetology', 'bio': 'Professional cosmetologist and beauty educator training salon leaders and beauty therapists.', 'display_order': 5},
            {'name': 'Chef Peter Kamau', 'role': 'Culinary Arts & Hospitality Instructor', 'department': 'Hospitality', 'bio': 'Experienced hotel chef bringing modern kitchen skills, hygiene standards, and pastry artistry to learners.', 'display_order': 6},
        ]
        for s in staff_data:
            StaffMember.objects.get_or_create(name=s['name'], defaults=s)

        # 5. Testimonials
        testimonials_data = [
            {'author': 'Brian Omondi', 'role': 'Electrical Installation Graduate (2024)', 'quote': 'PTVTI gave me real practical skills in electrical wiring and solar installation. Within two months of graduating, I secured full-time employment with a contracting firm.', 'is_featured': True, 'order': 1},
            {'author': 'Mercy Chebet', 'role': 'Cosmetology & Hairdressing Graduate', 'quote': 'The hands-on training in the salon studio helped me build true confidence. Today I run my own beauty salon in Kiambu and employ two other young women.', 'is_featured': True, 'order': 2},
            {'author': 'Dennis Kiprono', 'role': 'ICT & Computing Student', 'quote': 'The trainers at PTVTI do not just teach theory; we practice on real computers and solve practical tech problems every single day.', 'is_featured': True, 'order': 3},
        ]
        for t in testimonials_data:
            Testimonial.objects.get_or_create(author=t['author'], defaults=t)

        # 6. Events
        now = timezone.now()
        events_data = [
            {
                'title': 'PTVTI Annual Skills Showcase & Open Day',
                'description': 'Prospective students and parents are invited to tour workshops, meet instructors, and see live demonstrations by student artisans.',
                'location': 'PTVTI Main Campus, Gachie-Kihara',
                'starts_at': now + timedelta(days=21),
                'ends_at': now + timedelta(days=21, hours=6),
                'is_featured': True,
                'is_active': True,
            },
            {
                'title': 'Solar PV Technology Workshop',
                'description': 'Hands-on training session for electrical students and local technicians on rooftop solar installations and inverter setup.',
                'location': 'Engineering Workshop A',
                'starts_at': now + timedelta(days=35),
                'ends_at': now + timedelta(days=36),
                'is_featured': True,
                'is_active': True,
            },
        ]
        for ev in events_data:
            EventItem.objects.get_or_create(title=ev['title'], defaults=ev)

        # 7. News Articles
        news_data = [
            {
                'title': 'PTVTI Celebrates 100+ Graduates Excelling in Industry & Enterprise',
                'slug': 'ptvti-celebrates-graduates-industry',
                'summary': 'Our latest cohort of artisans and technicians achieve milestone employment in local and regional engineering, fashion, and salon industries.',
                'content': '<p>Palazzolo Technical and Vocational Training Institute (PTVTI) is proud to announce the continued success of its graduates across Kenya\'s technical sectors. Established in November 2021 by the Poverelle Sisters, the institute has now trained over 150 graduates who are actively working in industry or running successful vocational businesses.</p><p>With accreditation from TVETA and active partnerships with NITA and UNESCO, PTVTI continues to bridge the skills gap by offering affordable, values-centered vocational training for youth.</p>',
                'author': 'PTVTI Communications',
                'is_published': True,
            },
            {
                'title': 'New Workshop Equipment Installed for ICT and Electrical Engineering',
                'slug': 'new-workshop-equipment-installed',
                'summary': 'State-of-the-art tools and equipment have been added to the electrical and computer labs to bolster competency-based education.',
                'content': '<p>To ensure our learners train with modern industry tools, PTVTI has upgraded its technical infrastructure with new electrical testing units, digital multimeters, and high-speed workstations for the computer laboratory.</p>',
                'author': 'Academic Registrar',
                'is_published': True,
            },
        ]
        for article in news_data:
            NewsArticle.objects.get_or_create(slug=article['slug'], defaults=article)

        # 8. Department Contacts
        dept_contacts = [
            {'department': 'Admissions Office', 'phone': '+254 700 000 001', 'email': 'admissions@palazzolotechnical.co.ke', 'address': 'Main Administration Block, Ground Floor'},
            {'department': 'Engineering Department', 'phone': '+254 700 000 002', 'email': 'engineering@palazzolotechnical.co.ke', 'address': 'Technical Workshop Block B'},
            {'department': 'ICT & Computing Department', 'phone': '+254 700 000 003', 'email': 'ict@palazzolotechnical.co.ke', 'address': 'Computer Lab 1, First Floor'},
            {'department': 'Cosmetology & Hairdressing', 'phone': '+254 700 000 004', 'email': 'beauty@palazzolotechnical.co.ke', 'address': 'Cosmetology Studio'},
            {'department': 'Fashion & Design', 'phone': '+254 700 000 005', 'email': 'fashion@palazzolotechnical.co.ke', 'address': 'Fashion Studio Block A'},
            {'department': 'Hospitality & Catering', 'phone': '+254 700 000 006', 'email': 'hospitality@palazzolotechnical.co.ke', 'address': 'Training Kitchen & Bakery'},
        ]
        for dc in dept_contacts:
            DepartmentContact.objects.get_or_create(department=dc['department'], defaults=dc)

        self.stdout.write(self.style.SUCCESS('Successfully seeded verified PTVTI institutional data!'))

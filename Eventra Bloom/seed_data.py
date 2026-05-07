"""
Seed script — run: python seed_data.py
from inside the college_events directory
"""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_events.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, time, timedelta
from events.models import Category, Event, Registration, Announcement

print("🌱 Seeding database...")

# Admin user
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@college.edu', 'admin123', first_name='Admin', last_name='User')
    print("✅ Admin created: admin / admin123")
else:
    admin = User.objects.get(username='admin')

# Student users
students = []
student_data = [
    ('alice', 'Alice', 'Johnson', 'alice@college.edu'),
    ('bob', 'Bob', 'Smith', 'bob@college.edu'),
    ('carol', 'Carol', 'Davis', 'carol@college.edu'),
    ('dan', 'Dan', 'Wilson', 'dan@college.edu'),
]
for uname, first, last, email in student_data:
    u, created = User.objects.get_or_create(username=uname, defaults={'first_name': first, 'last_name': last, 'email': email})
    if created:
        u.set_password('pass123')
        u.save()
    students.append(u)
print(f"✅ {len(students)} student accounts created (password: pass123)")

# Categories
cats_data = [
    ('Academic', '#B5EAD7', '📚'),
    ('Cultural', '#FFB3C6', '🎭'),
    ('Sports', '#FFDAB9', '🏆'),
    ('Technology', '#C9B8FF', '💻'),
    ('Social', '#B3D9FF', '🎉'),
    ('Music', '#FFF3B0', '🎵'),
]
cats = {}
for name, color, icon in cats_data:
    cat, _ = Category.objects.get_or_create(name=name, defaults={'color': color, 'icon': icon})
    cats[name] = cat
print(f"✅ {len(cats)} categories created")

# Events
now = timezone.now()
events_data = [
    {
        'title': 'Annual Tech Symposium 2024',
        'description': 'Join us for a day of cutting-edge technology talks, workshops, and networking with industry leaders. Topics include AI, blockchain, cloud computing, and cybersecurity. Refreshments will be provided throughout the day.',
        'category': 'Technology',
        'organizer': admin,
        'venue': 'Main Auditorium, Block A',
        'date': date.today() + timedelta(days=14),
        'start_time': time(9, 0),
        'end_time': time(17, 0),
        'max_participants': 300,
        'registration_deadline': now + timedelta(days=10),
        'status': 'upcoming',
        'is_featured': True,
    },
    {
        'title': 'Spring Cultural Fest',
        'description': 'Celebrate the vibrant cultures of our campus community! Enjoy traditional dances, music performances, art exhibitions, and a global food fair. Student clubs from 20+ cultural backgrounds will be showcasing their heritage.',
        'category': 'Cultural',
        'organizer': students[0],
        'venue': 'College Grounds',
        'date': date.today() + timedelta(days=7),
        'start_time': time(10, 0),
        'end_time': time(20, 0),
        'max_participants': 1000,
        'registration_deadline': now + timedelta(days=5),
        'status': 'upcoming',
        'is_featured': True,
    },
    {
        'title': 'Inter-College Basketball Tournament',
        'description': 'The biggest basketball event of the year! Eight college teams compete over three days for the championship trophy. Come cheer for our home team and enjoy the action-packed matches.',
        'category': 'Sports',
        'organizer': students[1],
        'venue': 'Sports Complex, Court 1',
        'date': date.today() + timedelta(days=21),
        'start_time': time(8, 0),
        'end_time': time(18, 0),
        'max_participants': 500,
        'registration_deadline': now + timedelta(days=15),
        'status': 'upcoming',
        'is_featured': False,
    },
    {
        'title': 'Research Paper Presentation',
        'description': 'An academic forum where students present their research papers across disciplines including engineering, science, humanities, and social sciences. Faculty judges will award prizes in each category.',
        'category': 'Academic',
        'organizer': admin,
        'venue': 'Seminar Hall, Block B',
        'date': date.today() + timedelta(days=30),
        'start_time': time(10, 0),
        'end_time': time(16, 0),
        'max_participants': 150,
        'registration_deadline': now + timedelta(days=25),
        'status': 'upcoming',
    },
    {
        'title': 'Campus Music Night',
        'description': 'An evening of live music featuring student bands and solo performers. Genres include classical, rock, indie, and fusion. Food stalls and a bonfire make this one of the most loved events of the year!',
        'category': 'Music',
        'organizer': students[2],
        'venue': 'Open Air Theatre',
        'date': date.today() + timedelta(days=5),
        'start_time': time(18, 0),
        'end_time': time(22, 0),
        'max_participants': 400,
        'registration_deadline': now + timedelta(days=3),
        'status': 'upcoming',
    },
    {
        'title': 'Python Workshop: From Beginner to Pro',
        'description': 'A hands-on full-day workshop covering Python fundamentals, data structures, file handling, web scraping, and an intro to Django. Bring your laptop! All skill levels welcome.',
        'category': 'Technology',
        'organizer': students[3],
        'venue': 'Computer Lab 3, Block C',
        'date': date.today() + timedelta(days=10),
        'start_time': time(9, 30),
        'end_time': time(17, 30),
        'max_participants': 60,
        'registration_deadline': now + timedelta(days=7),
        'status': 'upcoming',
    },
]

events = []
for data in events_data:
    cat = cats.get(data.pop('category'))
    ev, created = Event.objects.get_or_create(
        title=data['title'],
        defaults={**data, 'category': cat}
    )
    events.append(ev)

print(f"✅ {len(events)} events created")

# Registrations
reg_pairs = [(events[0], students[0]), (events[0], students[1]), (events[1], students[2]),
             (events[2], students[0]), (events[4], students[1]), (events[5], students[2]),
             (events[5], students[3]), (events[3], students[0])]
for event, student in reg_pairs:
    Registration.objects.get_or_create(event=event, user=student, defaults={'status': 'confirmed'})
print("✅ Sample registrations created")

# Announcements
Announcement.objects.get_or_create(
    title='Registration Now Open for Tech Symposium!',
    defaults={
        'content': 'We are thrilled to announce that registrations for the Annual Tech Symposium 2024 are now open. Early bird registrations get a free workshop seat!',
        'event': events[0],
        'created_by': admin,
        'is_pinned': True,
    }
)
Announcement.objects.get_or_create(
    title='New Events Added This Week',
    defaults={
        'content': 'Check out the latest additions — Campus Music Night and Python Workshop have just been listed. Spots are limited, register early!',
        'created_by': admin,
        'is_pinned': True,
    }
)
print("✅ Announcements created")
print("\n🎉 Database seeded successfully!")
print("\nCredentials:")
print("  Admin:   username=admin   password=admin123")
print("  Student: username=alice   password=pass123")
print("  Student: username=bob     password=pass123")

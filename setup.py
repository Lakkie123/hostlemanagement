#!/usr/bin/env python3
"""
HostelHub Setup Script
Run this once to set up the database, create admin, and add sample data.
"""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel_management.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User
from hostel_app.models import RoomType, Room, HostelFacility, Notice

print("🏠 Setting up HostelHub...")

# 1. Migrations
from django.core.management import call_command
call_command('makemigrations', '--noinput')
call_command('migrate', '--noinput')
print("✅ Database migrated")

# 2. Admin user
if not User.objects.filter(username='sahil').exists():
    User.objects.create_superuser('sahil', 'sahil@hostelhub.com', 'sahil@123',
                                  first_name='Sahil', last_name='Admin')
    print("✅ Admin created — username: sahil | password: sahil@123")
else:
    print("ℹ️  Admin 'sahil' already exists")

# 3. Room Types
room_types_data = [
    {'name': 'Single', 'capacity': 1, 'price_per_month': 3500,
     'description': 'Private single occupancy room with full privacy.'},
    {'name': 'Double Sharing', 'capacity': 2, 'price_per_month': 2500,
     'description': 'Shared room for two students.'},
    {'name': 'Triple Sharing', 'capacity': 3, 'price_per_month': 1800,
     'description': 'Economical shared room for three students.'},
    {'name': 'Dormitory', 'capacity': 6, 'price_per_month': 1200,
     'description': 'Large dormitory style room.'},
]
for rt in room_types_data:
    RoomType.objects.get_or_create(name=rt['name'], defaults=rt)
print("✅ Room types created")

# 4. Sample Rooms
single = RoomType.objects.get(name='Single')
double = RoomType.objects.get(name='Double Sharing')
triple = RoomType.objects.get(name='Triple Sharing')
dorm   = RoomType.objects.get(name='Dormitory')

rooms_data = [
    ('101', single, 1, True, True, True, False),
    ('102', double, 1, False, True, True, False),
    ('103', triple, 1, False, False, True, False),
    ('201', single, 2, True, True, True, True),
    ('202', double, 2, True, True, True, True),
    ('203', triple, 2, False, True, True, False),
    ('204', double, 2, False, False, True, False),
    ('301', single, 3, True, True, True, True),
    ('302', dorm,   3, False, False, True, False),
    ('303', triple, 3, True, True, True, False),
    ('401', single, 4, True, True, True, True),
    ('402', double, 4, True, True, True, True),
]
for rn, rt, fl, ac, bath, wifi, tv in rooms_data:
    Room.objects.get_or_create(room_number=rn, defaults={
        'room_type': rt, 'floor': fl,
        'has_ac': ac, 'has_attached_bathroom': bath,
        'has_wifi': wifi, 'has_tv': tv,
        'status': 'available',
    })
print("✅ Sample rooms created")

# 5. Facilities
facilities = [
    ('High-Speed WiFi', 'fa-wifi', '24/7 high-speed internet in all rooms and common areas.', '24 hours'),
    ('Dining Hall', 'fa-utensils', 'Nutritious home-style meals served three times a day.', '7:00 AM – 9:00 PM'),
    ('24/7 Security', 'fa-shield-halved', 'Round-the-clock security with CCTV and trained guards.', '24 hours'),
    ('Study Room', 'fa-book-open', 'Quiet, well-lit study rooms with comfortable seating.', '6:00 AM – 11:00 PM'),
    ('Laundry Service', 'fa-soap', 'Washing machines and dryers available for student use.', '8:00 AM – 8:00 PM'),
    ('Gym & Fitness', 'fa-dumbbell', 'Fully equipped gym with modern fitness equipment.', '5:30 AM – 10:00 PM'),
    ('Medical Room', 'fa-kit-medical', 'On-site nurse and first-aid facilities available.', '9:00 AM – 6:00 PM'),
    ('Common Room', 'fa-tv', 'Relax and socialize with TV, board games and lounge area.', '8:00 AM – 11:00 PM'),
]
for name, icon, desc, timing in facilities:
    HostelFacility.objects.get_or_create(name=name, defaults={
        'icon': icon, 'description': desc, 'timing': timing, 'is_active': True
    })
print("✅ Facilities created")

# 6. Sample Notice
admin_user = User.objects.get(username='sahil')
if not Notice.objects.exists():
    Notice.objects.create(
        title='Welcome to HostelHub!',
        content='We are happy to welcome all new students. Please visit the admin office for room allocation and queries.',
        category='general',
        posted_by=admin_user,
        is_active=True,
    )
    Notice.objects.create(
        title='Fee Payment Reminder',
        content='Monthly fees are due by the 5th of every month. Please ensure timely payment to avoid late charges.',
        category='fee',
        posted_by=admin_user,
        is_active=True,
    )
    print("✅ Sample notices created")

print("\n🎉 Setup complete!")
print("=" * 45)
print("  Run: python manage.py runserver")
print("  URL: http://127.0.0.1:8000/")
print("  Admin Panel: http://127.0.0.1:8000/admin-panel/")
print("  Admin Login: sahil / sahil@123")
print("=" * 45)

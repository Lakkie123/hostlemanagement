#!/usr/bin/env python
"""
Setup script to initialize the HostelHub database with sample data.
Run: python setup_data.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel_management.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from hostel_app.models import (RoomType, Room, StudentProfile,
                                HostelFacility, Notice, RoomAllocation, FeePayment)
from datetime import date, timedelta
from decimal import Decimal

print("🏠 Setting up HostelHub database...")

# ── Create Admin User ──────────────────────────────────────────────────
if not User.objects.filter(username='sahil').exists():
    admin = User.objects.create_superuser(
        username='sahil',
        password='sahil@123',
        email='sahil@hostelhub.com',
        first_name='Sahil',
        last_name='Admin'
    )
    print("✅ Admin user created: sahil / sahil@123")
else:
    print("ℹ️  Admin user 'sahil' already exists")

# ── Create Room Types ──────────────────────────────────────────────────
room_types_data = [
    {'name': 'Single', 'capacity': 1, 'price_per_month': Decimal('4500.00'),
     'description': 'Private single occupancy room with all amenities'},
    {'name': 'Double Sharing', 'capacity': 2, 'price_per_month': Decimal('3000.00'),
     'description': 'Comfortable double sharing room'},
    {'name': 'Triple Sharing', 'capacity': 3, 'price_per_month': Decimal('2200.00'),
     'description': 'Economical triple sharing room'},
    {'name': 'Dormitory', 'capacity': 6, 'price_per_month': Decimal('1500.00'),
     'description': 'Budget-friendly dormitory style accommodation'},
]

room_types = {}
for rt_data in room_types_data:
    rt, created = RoomType.objects.get_or_create(
        name=rt_data['name'],
        defaults=rt_data
    )
    room_types[rt.name] = rt
    if created:
        print(f"✅ Room type created: {rt.name}")

# ── Create Rooms ───────────────────────────────────────────────────────
rooms_data = [
    # Ground Floor Singles
    {'room_number': '101', 'room_type': 'Single', 'floor': 1, 'has_ac': True, 'has_wifi': True, 'has_attached_bathroom': True, 'has_tv': True, 'status': 'available'},
    {'room_number': '102', 'room_type': 'Single', 'floor': 1, 'has_ac': True, 'has_wifi': True, 'has_attached_bathroom': True, 'has_tv': False, 'status': 'available'},
    {'room_number': '103', 'room_type': 'Single', 'floor': 1, 'has_ac': False, 'has_wifi': True, 'has_attached_bathroom': False, 'has_tv': False, 'status': 'maintenance'},
    # Floor 1 Double Sharing
    {'room_number': '201', 'room_type': 'Double Sharing', 'floor': 2, 'has_ac': True, 'has_wifi': True, 'has_attached_bathroom': True, 'has_tv': False, 'status': 'available'},
    {'room_number': '202', 'room_type': 'Double Sharing', 'floor': 2, 'has_ac': False, 'has_wifi': True, 'has_attached_bathroom': False, 'has_tv': False, 'status': 'available'},
    {'room_number': '203', 'room_type': 'Double Sharing', 'floor': 2, 'has_ac': True, 'has_wifi': True, 'has_attached_bathroom': True, 'has_tv': True, 'status': 'available'},
    {'room_number': '204', 'room_type': 'Double Sharing', 'floor': 2, 'has_ac': False, 'has_wifi': True, 'has_attached_bathroom': False, 'has_tv': False, 'status': 'reserved'},
    # Floor 2 Triple Sharing
    {'room_number': '301', 'room_type': 'Triple Sharing', 'floor': 3, 'has_ac': False, 'has_wifi': True, 'has_attached_bathroom': False, 'has_tv': False, 'status': 'available'},
    {'room_number': '302', 'room_type': 'Triple Sharing', 'floor': 3, 'has_ac': True, 'has_wifi': True, 'has_attached_bathroom': True, 'has_tv': False, 'status': 'available'},
    {'room_number': '303', 'room_type': 'Triple Sharing', 'floor': 3, 'has_ac': False, 'has_wifi': True, 'has_attached_bathroom': False, 'has_tv': False, 'status': 'available'},
    # Floor 3 Dormitory
    {'room_number': '401', 'room_type': 'Dormitory', 'floor': 4, 'has_ac': False, 'has_wifi': True, 'has_attached_bathroom': False, 'has_tv': True, 'status': 'available'},
    {'room_number': '402', 'room_type': 'Dormitory', 'floor': 4, 'has_ac': False, 'has_wifi': True, 'has_attached_bathroom': False, 'has_tv': False, 'status': 'available'},
]

for r_data in rooms_data:
    rt_name = r_data.pop('room_type')
    r_data['room_type'] = room_types[rt_name]
    room, created = Room.objects.get_or_create(
        room_number=r_data['room_number'],
        defaults=r_data
    )
    if created:
        print(f"✅ Room created: {room.room_number} ({rt_name})")

# ── Create Sample Students ─────────────────────────────────────────────
students_data = [
    {
        'username': 'student1', 'password': 'student@123',
        'first_name': 'Rahul', 'last_name': 'Sharma',
        'email': 'rahul@example.com',
        'roll': 'CS2021001', 'phone': '9876543210',
        'gender': 'M', 'course': 'B.Tech Computer Science', 'year': 3,
        'guardian': 'Ramesh Sharma', 'g_phone': '9876543211',
        'status': 'active'
    },
    {
        'username': 'student2', 'password': 'student@123',
        'first_name': 'Priya', 'last_name': 'Patel',
        'email': 'priya@example.com',
        'roll': 'ME2022042', 'phone': '9876543220',
        'gender': 'F', 'course': 'B.Tech Mechanical', 'year': 2,
        'guardian': 'Suresh Patel', 'g_phone': '9876543221',
        'status': 'active'
    },
    {
        'username': 'student3', 'password': 'student@123',
        'first_name': 'Amit', 'last_name': 'Kumar',
        'email': 'amit@example.com',
        'roll': 'EC2023015', 'phone': '9876543230',
        'gender': 'M', 'course': 'B.Tech Electronics', 'year': 1,
        'guardian': 'Vijay Kumar', 'g_phone': '9876543231',
        'status': 'pending'
    },
]

admin_user = User.objects.get(username='sahil')
created_students = []

for s in students_data:
    if not User.objects.filter(username=s['username']).exists():
        user = User.objects.create_user(
            username=s['username'], password=s['password'],
            first_name=s['first_name'], last_name=s['last_name'],
            email=s['email']
        )
        from datetime import date as d
        profile = StudentProfile.objects.create(
            user=user, roll_number=s['roll'],
            phone=s['phone'], gender=s['gender'],
            course=s['course'], year_of_study=s['year'],
            guardian_name=s['guardian'], guardian_phone=s['g_phone'],
            address='123 Sample Street, City, State',
            date_of_birth=d(2000, 1, 15),
            status=s['status']
        )
        created_students.append(profile)
        print(f"✅ Student created: {s['username']} / {s['password']}")
    else:
        profile = StudentProfile.objects.filter(user__username=s['username']).first()
        if profile:
            created_students.append(profile)
        print(f"ℹ️  Student '{s['username']}' already exists")

# ── Create Room Allocations ────────────────────────────────────────────
active_students = [p for p in created_students if p.status == 'active']
available_rooms = Room.objects.filter(status='available')

for i, profile in enumerate(active_students):
    existing = RoomAllocation.objects.filter(student=profile, status='active').first()
    if not existing and i < available_rooms.count():
        room = available_rooms[i]
        alloc = RoomAllocation.objects.create(
            student=profile, room=room,
            allocated_date=date.today() - timedelta(days=30 * (i + 1)),
            expected_vacate_date=date.today() + timedelta(days=180),
            monthly_rent=room.room_type.price_per_month,
            security_deposit=room.room_type.price_per_month * 2,
            status='active',
            allocated_by=admin_user
        )
        room.current_occupancy += 1
        if room.current_occupancy >= room.room_type.capacity:
            room.status = 'occupied'
        room.save()

        # Add sample fee payment
        FeePayment.objects.create(
            allocation=alloc,
            amount=alloc.monthly_rent,
            payment_date=date.today() - timedelta(days=5),
            due_date=date.today(),
            month=date.today().strftime('%B %Y'),
            status='paid',
            payment_method='upi',
            transaction_id=f'TXN{i+1}00{i+1}XYZ',
            received_by=admin_user
        )
        print(f"✅ Allocation created: {profile.user.get_full_name()} → Room {room.room_number}")

# ── Create Hostel Facilities ───────────────────────────────────────────
facilities_data = [
    {'name': 'High-Speed WiFi', 'description': 'Unlimited high-speed internet access throughout the hostel premises, including rooms and common areas.', 'icon': 'fa-wifi', 'timing': '24/7'},
    {'name': 'Dining Hall', 'description': 'Nutritious and hygienic meals served three times daily. Special diets available on request.', 'icon': 'fa-utensils', 'timing': '7:00 AM – 10:00 PM'},
    {'name': '24/7 Security', 'description': 'Round-the-clock professional security with CCTV surveillance and biometric entry.', 'icon': 'fa-shield-halved', 'timing': '24 Hours'},
    {'name': 'Study Room', 'description': 'Dedicated air-conditioned study rooms with individual desks and reference library access.', 'icon': 'fa-book-open', 'timing': '6:00 AM – 12:00 AM'},
    {'name': 'Laundry Service', 'description': 'Fully-equipped laundry room with washing machines, dryers and ironing facilities.', 'icon': 'fa-shirt', 'timing': '7:00 AM – 9:00 PM'},
    {'name': 'Fitness Center', 'description': 'Modern gym with cardio equipment, weights and a dedicated yoga area.', 'icon': 'fa-dumbbell', 'timing': '5:00 AM – 10:00 PM'},
    {'name': 'Medical Room', 'description': 'On-site medical facility with qualified nurse and first-aid equipment. Doctor visits twice weekly.', 'icon': 'fa-kit-medical', 'timing': '8:00 AM – 8:00 PM'},
    {'name': 'Common Room', 'description': 'Recreational common room with TV, indoor games and comfortable seating for socialising.', 'icon': 'fa-couch', 'timing': '8:00 AM – 11:00 PM'},
]

for f_data in facilities_data:
    fac, created = HostelFacility.objects.get_or_create(
        name=f_data['name'], defaults=f_data
    )
    if created:
        print(f"✅ Facility created: {fac.name}")

# ── Create Sample Notices ──────────────────────────────────────────────
notices_data = [
    {
        'title': 'Monthly Rent Due – Pay Before 5th',
        'content': 'All residents are reminded that monthly rent is due by the 5th of each month. Late payments will attract a penalty of ₹100 per day.',
        'category': 'fee',
    },
    {
        'title': 'Hostel Day Celebration – 25th March',
        'content': 'We are pleased to announce Hostel Day celebrations on 25th March. Cultural programs, games and a special dinner are planned. All students are encouraged to participate.',
        'category': 'event',
    },
    {
        'title': 'Water Supply Interruption – 3rd Floor',
        'content': 'Due to maintenance work, water supply on the 3rd floor will be interrupted from 10 AM to 2 PM this Saturday. Residents are requested to store water in advance.',
        'category': 'maintenance',
    },
    {
        'title': 'New WiFi Password Updated',
        'content': 'The hostel WiFi password has been updated for security purposes. Please collect the new password from the warden\'s office with your ID card.',
        'category': 'general',
    },
]

for n_data in notices_data:
    notice, created = Notice.objects.get_or_create(
        title=n_data['title'],
        defaults={**n_data, 'posted_by': admin_user, 'is_active': True}
    )
    if created:
        print(f"✅ Notice created: {notice.title}")

print("\n" + "="*60)
print("🎉 HostelHub setup complete!")
print("="*60)
print("\n📋 Login Credentials:")
print("  Admin  → username: sahil       | password: sahil@123")
print("  Student→ username: student1    | password: student@123")
print("  Student→ username: student2    | password: student@123")
print("  Student→ username: student3    | password: student@123")
print("\n🌐 Run the server:")
print("  cd hostel_management")
print("  python manage.py runserver")
print("  Then open: http://127.0.0.1:8000/")
print("="*60)

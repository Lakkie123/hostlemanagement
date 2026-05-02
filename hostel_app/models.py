from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from cloudinary.models import CloudinaryField


class StudentProfile(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    roll_number = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    course = models.CharField(max_length=100, blank=True)
    year_of_study = models.IntegerField(default=1)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    profile_photo = CloudinaryField('Profile Photo', null=True, blank=True)
    aadhar_front = CloudinaryField('aadhar_front', resource_type='raw', null=True, blank=True)
    aadhar_back = CloudinaryField('aadhar_back', resource_type='raw', null=True, blank=True)
    income_certificate = CloudinaryField('income_certificate', resource_type='raw', null=True, blank=True)
    jeep_rank_card = CloudinaryField('jeep_rank_card', resource_type='raw', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"


class RoomType(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    amenities = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price_per_month}/month"


class Room(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('reserved', 'Reserved'),
    ]
    FLOOR_CHOICES = [(i, f'Floor {i}') for i in range(0, 11)]

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    floor = models.IntegerField(choices=FLOOR_CHOICES, default=1)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')
    current_occupancy = models.IntegerField(default=0)
    has_ac = models.BooleanField(default=False)
    has_attached_bathroom = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=True)
    has_tv = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_available(self):
        return self.current_occupancy < self.room_type.capacity and self.status == 'available'

    def occupancy_percent(self):
        if self.room_type.capacity == 0:
            return 0
        return int((self.current_occupancy / self.room_type.capacity) * 100)

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type.name})"


class RoomAllocation(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('vacated', 'Vacated'),
        ('transferred', 'Transferred'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='allocations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='allocations')
    allocated_date = models.DateField(default=timezone.now)
    expected_vacate_date = models.DateField(null=True, blank=True)
    actual_vacate_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    allocated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='allocations_made')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.get_full_name()} → Room {self.room.room_number}"

    class Meta:
        ordering = ['-created_at']


def slip_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    student_name = instance.allocation.student.user.get_full_name().replace(' ', '_')
    roll = instance.allocation.student.roll_number
    month = instance.month.replace(' ', '_')
    return f'fee_slips/{roll}_{student_name}_{month}.{ext}'


class FeePayment(models.Model):
    STATUS_CHOICES = [('paid', 'Paid'), ('pending', 'Pending'), ('overdue', 'Overdue')]
    PAYMENT_METHOD = [('cash', 'Cash'), ('online', 'Online'), ('cheque', 'Cheque'), ('upi', 'UPI')]

    allocation = models.ForeignKey(RoomAllocation, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    month = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD, default='cash')
    transaction_id = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    slip_image = models.ImageField(upload_to=slip_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.allocation.student} - {self.month} - ₹{self.amount}"


class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('maintenance', 'Maintenance'),
        ('cleanliness', 'Cleanliness'),
        ('security', 'Security'),
        ('food', 'Food'),
        ('electricity', 'Electricity'),
        ('plumbing', 'Plumbing'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='complaints')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    resolution_notes = models.TextField(blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} - {self.student}"

    class Meta:
        ordering = ['-created_at']


class Notice(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('maintenance', 'Maintenance'),
        ('event', 'Event'),
        ('fee', 'Fee'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default='general')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Visitor(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='visitors')
    visitor_name = models.CharField(max_length=100)
    visitor_phone = models.CharField(max_length=15)
    relation = models.CharField(max_length=50)
    purpose = models.CharField(max_length=200)
    check_in = models.DateTimeField(default=timezone.now)
    check_out = models.DateTimeField(null=True, blank=True)
    id_proof = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.visitor_name} visiting {self.student}"

    class Meta:
        ordering = ['-check_in']


class HostelFacility(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fa-check')
    is_active = models.BooleanField(default=True)
    timing = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Hostel Facilities'
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import StudentProfile, Room, RoomAllocation, FeePayment, Complaint, Notice, Visitor, RoomType


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    roll_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Roll Number'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    gender = forms.ChoiceField(choices=StudentProfile.GENDER_CHOICES)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    course = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Course Name'}))
    year_of_study = forms.IntegerField(min_value=1, max_value=6)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Permanent Address'}))
    guardian_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Guardian Name'}))
    guardian_phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Guardian Phone'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                roll_number=self.cleaned_data['roll_number'],
                phone=self.cleaned_data['phone'],
                gender=self.cleaned_data['gender'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                course=self.cleaned_data['course'],
                year_of_study=self.cleaned_data['year_of_study'],
                address=self.cleaned_data['address'],
                guardian_name=self.cleaned_data['guardian_name'],
                guardian_phone=self.cleaned_data['guardian_phone'],
            )
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'floor', 'status', 'has_ac', 'has_attached_bathroom', 'has_wifi', 'has_tv', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class RoomAllocationForm(forms.ModelForm):
    class Meta:
        model = RoomAllocation
        fields = ['student', 'room', 'allocated_date', 'expected_vacate_date', 'monthly_rent', 'security_deposit', 'notes']
        widgets = {
            'allocated_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_vacate_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.filter(status='available')
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['allocation', 'amount', 'payment_date', 'due_date', 'month', 'status', 'payment_method', 'transaction_id', 'notes']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['category', 'priority', 'subject', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your complaint in detail...'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Brief subject of the complaint'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'category', 'is_active', 'expires_at']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['visitor_name', 'visitor_phone', 'relation', 'purpose', 'id_proof']
        widgets = {
            'purpose': forms.TextInput(attrs={'placeholder': 'Purpose of visit'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = StudentProfile
        fields = ['phone', 'address', 'guardian_name', 'guardian_phone']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['first_name'].initial = instance.user.first_name
            self.fields['last_name'].initial = instance.user.last_name
            self.fields['email'].initial = instance.user.email
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

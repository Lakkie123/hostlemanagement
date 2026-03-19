# 🏠 HostelHub — Premium Hostel Management System

A full-featured Django hostel management system with a professional design, admin panel, student portal, room management, fee tracking, complaints, notices and more.

---

## 🚀 Quick Setup (5 Minutes)

### 1. Prerequisites
Make sure you have **Python 3.9+** installed.
```bash
python --version
```

### 2. Install Dependencies
```bash
cd hostel_management
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Load Sample Data (Recommended)
This creates the admin user, rooms, students, facilities, notices and sample data:
```bash
python setup_data.py
```

### 5. Start the Server
```bash
python manage.py runserver
```

### 6. Open in Browser
```
http://127.0.0.1:8000/
```

---

## 🔐 Login Credentials

| Role     | Username   | Password     | URL                        |
|----------|------------|--------------|----------------------------|
| Admin    | `sahil`    | `sahil@123`  | `/admin-panel/`            |
| Student  | `student1` | `student@123`| `/dashboard/`              |
| Student  | `student2` | `student@123`| `/dashboard/`              |

---

## 📦 Features

### Admin Panel (`/admin-panel/`)
| Feature              | Description                                              |
|----------------------|----------------------------------------------------------|
| 📊 Dashboard         | Stats overview, room status, recent activity             |
| 🛏️ Room Management   | Add, edit, view all rooms with amenities & status        |
| 🚪 Available Rooms   | Quick view of all currently available rooms              |
| 👥 Student Management| View all students, approve pending registrations         |
| 🔑 Room Allocations  | Assign rooms to students, mark vacated                   |
| 💰 Fee Management    | Record and track all fee payments with history           |
| ⚠️ Complaints        | View and resolve student complaints                      |
| 📢 Notices           | Post and manage announcements for students               |
| 👣 Visitor Log       | View all visitor registrations from students             |

### Student Portal (`/dashboard/`)
| Feature              | Description                                              |
|----------------------|----------------------------------------------------------|
| 🏠 Dashboard         | Overview of room, payments, complaints, notices          |
| 👤 My Profile        | View and update personal information                     |
| 🛏️ My Room           | Current room details and allocation info                 |
| 💳 Fee Payments      | View full payment history and pending dues               |
| 📝 Submit Complaint  | File a new complaint with priority and category          |
| 🔔 My Complaints     | Track status of all submitted complaints                 |
| 👥 Register Visitor  | Log visitor entry for hostel records                     |
| 📋 Visitor Log       | View all registered visitors                             |

### Public Pages
- `/` — Home page with facilities, notices and stats
- `/register/` — Student registration form
- `/login/` — Login for both admin and students

---

## 🗄️ Database Models

| Model            | Description                                    |
|------------------|------------------------------------------------|
| `StudentProfile` | Extended user profile with academic info       |
| `RoomType`       | Room categories (Single, Double, Triple, Dorm) |
| `Room`           | Individual rooms with amenities and status     |
| `RoomAllocation` | Student-to-room assignments                    |
| `FeePayment`     | Monthly rent payment records                   |
| `Complaint`      | Student complaints with priority and status    |
| `Notice`         | Admin announcements for students               |
| `Visitor`        | Visitor entry log per student                  |
| `HostelFacility` | Hostel amenities displayed on homepage         |

---

## 📁 Project Structure

```
hostel_management/
├── manage.py
├── requirements.txt
├── setup_data.py              ← Run this to seed sample data
├── hostel.db                  ← SQLite database (auto-created)
├── hostel_management/
│   ├── settings.py
│   └── urls.py
└── hostel_app/
    ├── models.py              ← All database models
    ├── views.py               ← All view logic
    ├── forms.py               ← Django forms
    ├── urls.py                ← URL routing
    ├── admin.py               ← Django admin config
    └── templates/
        └── hostel_app/
            ├── base.html      ← Main layout with navbar
            ├── home.html      ← Public homepage
            ├── login.html     ← Login page
            ├── register.html  ← Registration page
            ├── admin/         ← Admin panel templates
            └── student/       ← Student portal templates
```

---

## 🎨 Design

- **Theme**: Navy blue & gold — refined, professional, institutional
- **Fonts**: Playfair Display (headings) + DM Sans (body)
- **CSS**: Pure CSS with custom variables, no frameworks
- **Responsive**: Mobile-friendly sidebar and grid layouts
- **Animations**: Smooth fade-in-up on page load

---

## 🛠️ Tech Stack

- **Backend**: Python 3 + Django 4.2
- **Database**: SQLite 3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts

---

## 📝 Notes

- After registering as a student, wait for admin approval
- Admin can approve students from **Students → Pending Approvals**
- Room allocation must be done by admin after approval
- Django superuser panel also available at `/django-admin/`

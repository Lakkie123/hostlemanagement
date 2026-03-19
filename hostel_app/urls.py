from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Student URLs
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile/', views.student_profile, name='student_profile'),
    path('my-room/', views.my_room, name='my_room'),
    path('complaints/submit/', views.submit_complaint, name='submit_complaint'),
    path('complaints/my/', views.my_complaints, name='my_complaints'),
    path('payments/my/', views.my_payments, name='my_payments'),
    path('pay-fee/', views.pay_fee, name='pay_fee'),
    path('pay-fee/confirm/', views.confirm_payment, name='confirm_payment'),
    path('visitors/add/', views.add_visitor, name='add_visitor'),
    path('visitors/my/', views.my_visitors, name='my_visitors'),

    # Admin URLs
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/rooms/', views.manage_rooms, name='manage_rooms'),
    path('admin-panel/rooms/add/', views.add_room, name='add_room'),
    path('admin-panel/rooms/<int:pk>/edit/', views.edit_room, name='edit_room'),
    path('admin-panel/rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('admin-panel/rooms/available/', views.available_rooms, name='available_rooms'),
    path('admin-panel/students/', views.manage_students, name='manage_students'),
    path('admin-panel/students/<int:pk>/', views.student_detail, name='student_detail'),
    path('admin-panel/students/<int:pk>/approve/', views.approve_student, name='approve_student'),
    path('admin-panel/allocations/', views.manage_allocations, name='manage_allocations'),
    path('admin-panel/allocations/add/', views.add_allocation, name='add_allocation'),
    path('admin-panel/allocations/<int:pk>/vacate/', views.vacate_allocation, name='vacate_allocation'),
    path('admin-panel/fees/', views.manage_fees, name='manage_fees'),
    path('admin-panel/fees/add/', views.add_fee, name='add_fee'),
    path('admin-panel/complaints/', views.manage_complaints, name='manage_complaints'),
    path('admin-panel/complaints/<int:pk>/resolve/', views.resolve_complaint, name='resolve_complaint'),
    path('admin-panel/notices/', views.manage_notices, name='manage_notices'),
    path('admin-panel/notices/add/', views.add_notice, name='add_notice'),
    path('admin-panel/notices/<int:pk>/edit/', views.edit_notice, name='edit_notice'),
    path('admin-panel/visitors/', views.manage_visitors, name='manage_visitors'),
    path('admin-panel/fees/<int:pk>/verify/', views.verify_payment, name='verify_payment'),
    path('admin-panel/fees/pending/', views.pending_verifications, name='pending_verifications'),
    

    # API
    path('api/room-stats/', views.room_stats_api, name='room_stats_api'),
]

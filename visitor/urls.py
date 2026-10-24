from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', views.dashboard, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Parents
    path('parents/', views.parent_list, name='parent_list'),
    path('parents/add/', views.parent_add, name='parent_add'),
    path('parents/<int:pk>/edit/', views.parent_edit, name='parent_edit'),
    path('parents/<int:pk>/delete/', views.parent_delete, name='parent_delete'),

    # Teachers
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.teacher_add, name='teacher_add'),
    path('teachers/<int:pk>/edit/', views.teacher_edit, name='teacher_edit'),
    path('teachers/<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),

    # Visits
    path('visits/', views.visit_list, name='visit_list'),

    # Settings
    path('settings/', views.settings_view, name='settings_view'),

    # ==================== RFID API (for ESP32) ====================
    path('api/rfid/', views.api_rfid_scan, name='api_rfid'),
    path('api/reminder/', views.api_check_reminders, name='api_reminder'),
    path('api/force-end/', views.api_force_end, name='api_force_end'),
    path('api/status/', views.api_status, name='api_status'),
    path('api-tester/', views.api_tester, name='api_tester'),
]
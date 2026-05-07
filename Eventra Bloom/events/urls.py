from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:pk>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:pk>/delete/', views.delete_event, name='delete_event'),
    path('events/<int:pk>/register/', views.register_event, name='register_event'),
    path('registrations/<int:pk>/cancel/', views.cancel_registration, name='cancel_registration'),
    path('my-events/', views.my_events, name='my_events'),
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    # Admin auth
    path('admin-login/', views.admin_login_view, name='admin_login'),
    # Admin panel
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/events/', views.admin_events, name='admin_events'),
    path('admin-panel/events/<int:pk>/edit/', views.admin_edit_event, name='admin_edit_event'),
    path('admin-panel/events/<int:pk>/delete/', views.admin_delete_event, name='admin_delete_event'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/users/<int:pk>/toggle-staff/', views.admin_toggle_staff, name='admin_toggle_staff'),
    path('admin-panel/users/<int:pk>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('admin-panel/registrations/', views.admin_registrations, name='admin_registrations'),
    path('admin-panel/registrations/<int:pk>/update/', views.admin_update_registration, name='admin_update_registration'),
    path('admin-panel/categories/', views.admin_categories, name='admin_categories'),
    path('admin-panel/categories/<int:pk>/edit/', views.admin_edit_category, name='admin_edit_category'),
    path('admin-panel/categories/<int:pk>/delete/', views.admin_delete_category, name='admin_delete_category'),
    path('admin-panel/announcements/', views.admin_announcements, name='admin_announcements'),
    path('admin-panel/announcements/<int:pk>/delete/', views.admin_delete_announcement, name='admin_delete_announcement'),
    # Legacy + API
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/events/', views.api_events, name='api_events'),
]

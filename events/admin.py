from django.contrib import admin
from .models import Event, Category, Registration, Announcement, StudentProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'organizer', 'date', 'status', 'registered_count', 'is_featured']
    list_filter = ['status', 'category', 'date']
    search_fields = ['title', 'description', 'venue']
    list_editable = ['status', 'is_featured']
    date_hierarchy = 'date'


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'registered_at']
    list_filter = ['status', 'registered_at']
    search_fields = ['user__username', 'event__title']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'event', 'created_by', 'created_at', 'is_pinned']
    list_editable = ['is_pinned']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'roll_no', 'branch', 'year', 'semester', 'course']
    search_fields = ['user__username', 'user__first_name', 'roll_no']
    list_filter = ['branch', 'year', 'semester']

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default='#FFB3C6')
    icon = models.CharField(max_length=50, default='🎉')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    venue = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_participants = models.PositiveIntegerField(default=100)
    registration_deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    image_url = models.CharField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def registered_count(self):
        return self.registrations.filter(status='confirmed').count()

    @property
    def spots_left(self):
        return self.max_participants - self.registered_count

    @property
    def is_registration_open(self):
        return timezone.now() < self.registration_deadline and self.spots_left > 0

    class Meta:
        ordering = ['date', 'start_time']


class Registration(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('waitlisted', 'Waitlisted'),
        ('cancelled', 'Cancelled'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    registered_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.event.title}"

    class Meta:
        unique_together = ['event', 'user']


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='announcements', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-is_pinned', '-created_at']

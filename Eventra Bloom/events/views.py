from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .models import Event, Category, Registration, Announcement

ADMIN_SECRET_CODE = "EVENTRA2026"  # Change this to your desired admin code


# ─────────────────────────────────────────────
#  Public / Student Views
# ─────────────────────────────────────────────

def home(request):
    featured_events = Event.objects.filter(is_featured=True, status='upcoming')[:3]
    upcoming_events = Event.objects.filter(status='upcoming', date__gte=timezone.now().date()).order_by('date')[:6]
    categories = Category.objects.annotate(event_count=Count('event')).all()
    announcements = Announcement.objects.filter(is_pinned=True)[:3]
    total_events = Event.objects.count()
    total_students = User.objects.filter(is_staff=False).count()
    total_registrations = Registration.objects.filter(status='confirmed').count()
    context = {
        'featured_events': featured_events,
        'upcoming_events': upcoming_events,
        'categories': categories,
        'announcements': announcements,
        'stats': {
            'total_events': total_events,
            'total_students': total_students,
            'total_registrations': total_registrations,
        }
    }
    return render(request, 'events/home.html', context)


def event_list(request):
    events = Event.objects.all()
    category_id = request.GET.get('category')
    status = request.GET.get('status')
    search = request.GET.get('search')
    if category_id:
        events = events.filter(category_id=category_id)
    if status:
        events = events.filter(status=status)
    if search:
        events = events.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(venue__icontains=search))
    categories = Category.objects.all()
    context = {'events': events, 'categories': categories, 'selected_category': category_id, 'selected_status': status, 'search': search}
    return render(request, 'events/event_list.html', context)


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user_registration = None
    if request.user.is_authenticated:
        user_registration = Registration.objects.filter(event=event, user=request.user).first()
    announcements = event.announcements.all()
    related_events = Event.objects.filter(category=event.category).exclude(pk=pk)[:3]
    context = {'event': event, 'user_registration': user_registration, 'announcements': announcements, 'related_events': related_events}
    return render(request, 'events/event_detail.html', context)


@login_required
def register_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not event.is_registration_open:
        messages.error(request, 'Registration is closed for this event.')
        return redirect('event_detail', pk=pk)
    existing = Registration.objects.filter(event=event, user=request.user).first()
    if existing:
        messages.warning(request, 'You are already registered for this event.')
        return redirect('event_detail', pk=pk)
    Registration.objects.create(event=event, user=request.user, status='confirmed')
    messages.success(request, f'Successfully registered for {event.title}!')
    return redirect('event_detail', pk=pk)


@login_required
def cancel_registration(request, pk):
    registration = get_object_or_404(Registration, pk=pk, user=request.user)
    registration.status = 'cancelled'
    registration.save()
    messages.success(request, 'Registration cancelled successfully.')
    return redirect('my_events')


@login_required
def my_events(request):
    registrations = Registration.objects.filter(user=request.user).select_related('event').order_by('-registered_at')
    organized = Event.objects.filter(organizer=request.user).order_by('-date')
    context = {'registrations': registrations, 'organized_events': organized}
    return render(request, 'events/my_events.html', context)


@login_required
def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        venue = request.POST.get('venue')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        max_participants = request.POST.get('max_participants', 100)
        registration_deadline = request.POST.get('registration_deadline')
        category = Category.objects.get(pk=category_id) if category_id else None
        event = Event.objects.create(
            title=title, description=description, category=category,
            organizer=request.user, venue=venue, date=date,
            start_time=start_time, end_time=end_time,
            max_participants=max_participants,
            registration_deadline=registration_deadline,
        )
        messages.success(request, f'Event "{title}" created successfully!')
        return redirect('event_detail', pk=event.pk)
    categories = Category.objects.all()
    return render(request, 'events/create_event.html', {'categories': categories})


@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk, organizer=request.user)
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        event.venue = request.POST.get('venue')
        event.date = request.POST.get('date')
        event.start_time = request.POST.get('start_time')
        event.end_time = request.POST.get('end_time')
        event.max_participants = request.POST.get('max_participants', 100)
        event.registration_deadline = request.POST.get('registration_deadline')
        event.status = request.POST.get('status', 'upcoming')
        category_id = request.POST.get('category')
        event.category = Category.objects.get(pk=category_id) if category_id else None
        event.save()
        messages.success(request, 'Event updated successfully!')
        return redirect('event_detail', pk=event.pk)
    categories = Category.objects.all()
    return render(request, 'events/edit_event.html', {'event': event, 'categories': categories})


@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk, organizer=request.user)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('event_list')
    return render(request, 'events/confirm_delete.html', {'event': event})


# ─────────────────────────────────────────────
#  Auth Views
# ─────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'events/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            messages.success(request, f'Welcome, {first_name}! Your account has been created.')
            return redirect('home')
    return render(request, 'events/register.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# ─────────────────────────────────────────────
#  Admin Login (with secret code)
# ─────────────────────────────────────────────

def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin_code = request.POST.get('admin_code', '').strip()

        if admin_code != ADMIN_SECRET_CODE:
            messages.error(request, 'Invalid admin access code.')
            return render(request, 'events/admin_login.html')

        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}! Admin panel ready.')
            return redirect('admin_panel')
        elif user and not user.is_staff:
            messages.error(request, 'This account does not have admin privileges.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'events/admin_login.html')


def admin_required(view_func):
    """Decorator: must be logged in as staff."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.error(request, 'Admin access required. Please login with admin credentials.')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


# ─────────────────────────────────────────────
#  Admin Panel Views
# ─────────────────────────────────────────────

@admin_required
def admin_panel(request):
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(status='upcoming').count()
    ongoing_events = Event.objects.filter(status='ongoing').count()
    completed_events = Event.objects.filter(status='completed').count()
    total_users = User.objects.filter(is_staff=False).count()
    total_registrations = Registration.objects.filter(status='confirmed').count()
    total_categories = Category.objects.count()
    total_announcements = Announcement.objects.count()
    recent_events = Event.objects.order_by('-created_at')[:6]
    recent_registrations = Registration.objects.select_related('user', 'event').order_by('-registered_at')[:6]
    popular_events = Event.objects.annotate(reg_count=Count('registrations')).order_by('-reg_count')[:5]
    recent_users = User.objects.filter(is_staff=False).order_by('-date_joined')[:5]
    context = {
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'ongoing_events': ongoing_events,
        'completed_events': completed_events,
        'total_users': total_users,
        'total_registrations': total_registrations,
        'total_categories': total_categories,
        'total_announcements': total_announcements,
        'recent_events': recent_events,
        'recent_registrations': recent_registrations,
        'popular_events': popular_events,
        'recent_users': recent_users,
    }
    return render(request, 'events/admin_panel.html', context)


@admin_required
def admin_events(request):
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    category_filter = request.GET.get('category', '')
    events = Event.objects.select_related('category', 'organizer').annotate(reg_count=Count('registrations'))
    if search:
        events = events.filter(Q(title__icontains=search) | Q(venue__icontains=search))
    if status_filter:
        events = events.filter(status=status_filter)
    if category_filter:
        events = events.filter(category_id=category_filter)
    events = events.order_by('-created_at')
    categories = Category.objects.all()
    context = {'events': events, 'categories': categories, 'search': search, 'status_filter': status_filter, 'category_filter': category_filter}
    return render(request, 'events/admin_events.html', context)


@admin_required
def admin_edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        event.venue = request.POST.get('venue')
        event.date = request.POST.get('date')
        event.start_time = request.POST.get('start_time')
        event.end_time = request.POST.get('end_time')
        event.max_participants = request.POST.get('max_participants', 100)
        event.registration_deadline = request.POST.get('registration_deadline')
        event.status = request.POST.get('status', 'upcoming')
        event.is_featured = request.POST.get('is_featured') == 'on'
        category_id = request.POST.get('category')
        event.category = Category.objects.get(pk=category_id) if category_id else None
        event.save()
        messages.success(request, f'Event "{event.title}" updated successfully!')
        return redirect('admin_events')
    categories = Category.objects.all()
    return render(request, 'events/admin_edit_event.html', {'event': event, 'categories': categories})


@admin_required
def admin_delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        title = event.title
        event.delete()
        messages.success(request, f'Event "{title}" deleted.')
        return redirect('admin_events')
    return render(request, 'events/admin_confirm_delete.html', {'object': event, 'type': 'Event'})


@admin_required
def admin_users(request):
    search = request.GET.get('search', '')
    users = User.objects.annotate(
        reg_count=Count('registrations'),
        event_count=Count('organized_events')
    ).order_by('-date_joined')
    if search:
        users = users.filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search))
    context = {'users': users, 'search': search}
    return render(request, 'events/admin_users.html', context)


@admin_required
def admin_toggle_staff(request, pk):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            messages.error(request, "You can't change your own staff status.")
        else:
            user.is_staff = not user.is_staff
            user.save()
            status = 'granted admin access to' if user.is_staff else 'removed admin access from'
            messages.success(request, f'Successfully {status} {user.username}.')
    return redirect('admin_users')


@admin_required
def admin_delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if user == request.user:
            messages.error(request, "You can't delete your own account.")
            return redirect('admin_users')
        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" deleted.')
        return redirect('admin_users')
    return render(request, 'events/admin_confirm_delete.html', {'object': user, 'type': 'User'})


@admin_required
def admin_registrations(request):
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    registrations = Registration.objects.select_related('user', 'event').order_by('-registered_at')
    if search:
        registrations = registrations.filter(
            Q(user__username__icontains=search) | Q(user__first_name__icontains=search) |
            Q(event__title__icontains=search)
        )
    if status_filter:
        registrations = registrations.filter(status=status_filter)
    context = {'registrations': registrations, 'search': search, 'status_filter': status_filter}
    return render(request, 'events/admin_registrations.html', context)


@admin_required
def admin_update_registration(request, pk):
    if request.method == 'POST':
        reg = get_object_or_404(Registration, pk=pk)
        reg.status = request.POST.get('status', reg.status)
        reg.save()
        messages.success(request, 'Registration status updated.')
    return redirect('admin_registrations')


@admin_required
def admin_categories(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        color = request.POST.get('color', '#FFB3C6')
        icon = request.POST.get('icon', '🎉')
        if name:
            Category.objects.create(name=name, color=color, icon=icon)
            messages.success(request, f'Category "{name}" created.')
        return redirect('admin_categories')
    categories = Category.objects.annotate(event_count=Count('event')).order_by('name')
    context = {'categories': categories}
    return render(request, 'events/admin_categories.html', context)


@admin_required
def admin_edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.name = request.POST.get('name', category.name)
        category.color = request.POST.get('color', category.color)
        category.icon = request.POST.get('icon', category.icon)
        category.save()
        messages.success(request, f'Category "{category.name}" updated.')
        return redirect('admin_categories')
    return render(request, 'events/admin_edit_category.html', {'category': category})


@admin_required
def admin_delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'Category "{name}" deleted.')
        return redirect('admin_categories')
    return render(request, 'events/admin_confirm_delete.html', {'object': category, 'type': 'Category'})


@admin_required
def admin_announcements(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        event_id = request.POST.get('event')
        is_pinned = request.POST.get('is_pinned') == 'on'
        if title and content:
            event = Event.objects.get(pk=event_id) if event_id else None
            Announcement.objects.create(title=title, content=content, event=event, created_by=request.user, is_pinned=is_pinned)
            messages.success(request, f'Announcement "{title}" created.')
        return redirect('admin_announcements')
    announcements = Announcement.objects.select_related('created_by', 'event').order_by('-created_at')
    events = Event.objects.filter(status='upcoming').order_by('date')
    context = {'announcements': announcements, 'events': events}
    return render(request, 'events/admin_announcements.html', context)


@admin_required
def admin_delete_announcement(request, pk):
    ann = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        ann.delete()
        messages.success(request, 'Announcement deleted.')
        return redirect('admin_announcements')
    return render(request, 'events/admin_confirm_delete.html', {'object': ann, 'type': 'Announcement'})


# ─────────────────────────────────────────────
#  Legacy dashboard + API
# ─────────────────────────────────────────────

@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    return redirect('admin_panel')


def api_events(request):
    events = Event.objects.filter(status='upcoming').values('id', 'title', 'date', 'start_time', 'venue', 'max_participants')
    return JsonResponse({'events': list(events)}, safe=False)

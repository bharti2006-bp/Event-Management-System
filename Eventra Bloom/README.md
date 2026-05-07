# 🌸 EventBloom — College Event Management System

A full-featured college event management web application built with Django, SQLite, and a beautiful pastel-themed frontend.

## ✨ Features

| Feature | Details |
|---|---|
| **Event Management** | Create, edit, delete, and view events with categories |
| **Registration System** | Students can register/cancel for events with capacity tracking |
| **User Auth** | Signup, login, logout with role-based access (admin/student) |
| **Dashboard** | Admin analytics: stats, popular events, recent registrations |
| **Announcements** | Pinnable announcements linked to events |
| **Categories** | Color-coded event categories with icons |
| **Search & Filter** | Filter by category, status, and keyword search |
| **Responsive UI** | Works beautifully on mobile, tablet, and desktop |

## 🎨 Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript (pastel design system)
- **Backend**: Python 3.10+ / Django 4.2
- **Database**: SQLite (via Django ORM)
- **Fonts**: Playfair Display + DM Sans (Google Fonts)

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run database migrations
```bash
cd college_events
python manage.py makemigrations
python manage.py migrate
```

### 3. Seed sample data (optional but recommended)
```bash
python seed_data.py
```

### 4. Start the development server
```bash
python manage.py runserver
```

### 5. Open in browser
```
http://127.0.0.1:8000
```

## 🔑 Default Credentials

After running `seed_data.py`:

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Student | `alice` | `pass123` |
| Student | `bob` | `pass123` |
| Student | `carol` | `pass123` |

Admin panel: `http://127.0.0.1:8000/admin/`
Dashboard: `http://127.0.0.1:8000/dashboard/` (admin only)

## 📁 Project Structure

```
college_events/
├── college_events/          # Django project config
│   ├── settings.py          # Settings (SQLite, static files)
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py
├── events/                  # Main app
│   ├── models.py            # Event, Category, Registration, Announcement
│   ├── views.py             # All view logic
│   ├── urls.py              # App URL patterns
│   └── admin.py             # Django admin config
├── templates/events/        # HTML templates
│   ├── base.html            # Base layout with navbar/footer
│   ├── home.html            # Landing page
│   ├── event_list.html      # Browse/filter events
│   ├── event_detail.html    # Event page + registration
│   ├── create_event.html    # Create event form
│   ├── edit_event.html      # Edit event form
│   ├── my_events.html       # Student's registrations & events
│   ├── dashboard.html       # Admin dashboard
│   ├── login.html           # Login page
│   ├── register.html        # Signup page
│   └── partials/
│       └── event_card.html  # Reusable event card component
├── static/
│   ├── css/style.css        # Full pastel design system
│   └── js/main.js           # Interactions, animations
├── seed_data.py             # Sample data loader
├── manage.py
└── requirements.txt
```

## 🗄️ Database Models

### Event
- Title, description, category, organizer
- Date, start/end time, venue
- Max participants, registration deadline
- Status (upcoming/ongoing/completed/cancelled)
- Featured flag

### Category
- Name, color (hex), icon (emoji)

### Registration
- Links User ↔ Event
- Status: confirmed / waitlisted / cancelled
- Timestamp + notes

### Announcement
- Title, content, linked event (optional)
- Pinnable, timestamped

## 🌈 Design System

The pastel UI uses CSS custom properties:

```css
--pink:       #FFB3C6   /* Soft rose */
--lavender:   #C9B8FF   /* Light purple */
--mint:       #B5EAD7   /* Fresh green */
--peach:      #FFDAB9   /* Warm peach */
--sky:        #B3D9FF   /* Light blue */
--yellow:     #FFF3B0   /* Soft lemon */
```

## 📱 Pages

| URL | Page |
|-----|------|
| `/` | Home / Landing |
| `/events/` | Browse all events |
| `/events/<id>/` | Event detail + registration |
| `/events/create/` | Create new event |
| `/events/<id>/edit/` | Edit event |
| `/my-events/` | My registrations & organized events |
| `/dashboard/` | Admin dashboard |
| `/login/` | Login |
| `/register/` | Sign up |
| `/admin/` | Django admin |

---

## 🛡️ Admin Panel (New Feature)

### Admin Login
- URL: `/admin-login/`
- Requires: Username, Password, AND **Admin Access Code**
- Default admin code: `ADMIN2024`
- To change the code: edit `ADMIN_SECRET_CODE` in `events/views.py`

### Admin Panel Pages
| URL | Page |
|-----|------|
| `/admin-panel/` | Dashboard with stats |
| `/admin-panel/events/` | Manage all events |
| `/admin-panel/users/` | Manage users & roles |
| `/admin-panel/registrations/` | View/update registrations |
| `/admin-panel/categories/` | Create/edit categories |
| `/admin-panel/announcements/` | Post announcements |

### Create a superuser (first time setup)
```bash
python manage.py createsuperuser
```

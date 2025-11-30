# WheelDeals 🚗

A comprehensive Django-based online car marketplace with advanced features including vehicle inspection management, ad moderation, and role-based access control.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation (Windows)](#installation-windows)
- [Project Structure](#project-structure)
- [User Roles](#user-roles)
- [Usage Guide](#usage-guide)
- [Admin Panel](#admin-panel)
- [Troubleshooting](#troubleshooting)
- [Documentation](#documentation)

---

## ✨ Features

### Core Features

- 🔐 **User Authentication**: Registration, login, logout with role-based access
- 🚙 **Car Listings**: Create, view, edit, delete car advertisements
- 🔍 **Advanced Search**: Filter by make, model, price range, year
- 👤 **User Profiles**: Manage personal information and preferences
- 🖼️ **Image Upload**: Multiple images per car listing

### Advanced Features

- ✅ **Vehicle Inspection System**:
  - 3-phase workflow (Request → Accept → Inspect → Report)
  - Professional inspection with 14 component ratings
  - Photo uploads and detailed reports
  - Public inspection reports on car listings
- 👨‍💼 **Admin Panel**:

  - Ad moderation (pending/published/declined)
  - User management (roles & permissions)
  - Inspection oversight
  - Analytics dashboard with charts
  - System-wide management

- 🔐 **Role-Based Access**:
  - **Buyer**: Browse cars, request inspections
  - **Seller**: Post listings, manage ads
  - **Inspector**: Perform inspections, submit reports
  - **Admin**: Full system management

---

## 🛠️ Tech Stack

- **Backend**: Django 5.2.8 (Python web framework)
- **Database**: SQLite (development)

- **Frontend**: Bootstrap 5.3, Font Awesome icons
- **Charts**: Chart.js for analytics visualization
- **Image Processing**: Pillow 12.0.0

---

## 📌 Prerequisites

Before you begin, ensure you have the following installed on your Windows machine:

- **Python 3.12+**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/download/win)
- **PowerShell**: (Built-in on Windows 10/11)

---

## 🚀 Installation (Windows)

### Step 1: Clone the Repository

Open PowerShell and run:

```powershell
# Navigate to your desired directory
cd C:\Users\YourUsername\Documents

# Clone the repository
git clone https://github.com/Bilal-Ayub/WheelDeals.git

# Navigate into the project
cd WheelDeals
```

### Step 2: Create Virtual Environment

```powershell
# Create virtual environment
python -m venv my_env

# Activate virtual environment
.\my_env\Scripts\Activate.ps1
```

**Note**: If you get a PowerShell execution policy error, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies

```powershell
# Upgrade pip (optional but recommended)
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**Dependencies installed**:

- Django 5.2.8
- Pillow 12.0.0
- asgiref 3.10.0
- sqlparse 0.5.3
- tzdata 2025.2

### Step 4: Database Setup

```powershell
# Apply database migrations
python manage.py migrate

# Create admin user
python create_admin.py
```

When prompted:

- **Username**: Press Enter for default (`admin`)
- **Password**: Press Enter for default (`admin123`)
- **Email**: Press Enter for default (`admin@wheeldeals.com`)

**Or manually create via Django shell**:

```powershell
python manage.py shell
```

Then run:

```python
from users.models import CustomUser
admin = CustomUser.objects.create_user(
    username='admin',
    password='admin123',
    email='admin@wheeldeals.com',
    first_name='Admin',
    last_name='User',
    role='admin'
)
print(f"✓ Admin created: {admin.username}")
exit()
```

### Step 5: Run the Development Server

```powershell
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

**🎉 That's it! You're ready to use WheelDeals!**

---

## 📁 Project Structure

```
wheeldeals/
├── admin_panel/              # Admin dashboard & management
│   ├── views.py              # Admin views (dashboard, moderation, etc.)
│   ├── urls.py               # Admin URL patterns
│   ├── decorators.py         # @admin_required decorator
│   └── templates/            # Admin panel templates
├── cars/                     # Car listing functionality
│   ├── models.py             # Car model with status field
│   ├── views.py              # CRUD operations for cars
│   ├── forms.py              # Car listing forms
│   └── templates/            # Car-related templates
├── inspections/              # Vehicle inspection system
│   ├── models.py             # InspectionRequest, Report, Photo models
│   ├── views.py              # Inspection workflow views
│   ├── forms.py              # Inspection forms
│   └── templates/            # Inspection templates
├── users/                    # User management & authentication
│   ├── models.py             # Custom User model with roles
│   ├── views.py              # Auth views (login, register, profile)
│   ├── forms.py              # User forms (signup excludes admin role)
│   └── templates/            # User-related templates
├── wheeldeals_project/       # Django project settings
│   ├── settings.py           # Project configuration
│   ├── urls.py               # Main URL routing
│   └── wsgi.py               # WSGI configuration
├── templates/                # Global templates
│   ├── base.html             # Base template with navbar
│   └── home.html             # Homepage
├── media/                    # Uploaded images (cars, inspections)
├── static/                   # Static files (CSS, JS)
├── db.sqlite3                # SQLite database
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── create_admin.py           # Admin user creation script
├── verify_admin_data.py      # Data verification script
└── Documentation/
    ├── ADMIN_ROLE_GUIDE.md
    ├── ADMIN_QUICKSTART.md
    ├── ADMIN_TESTING_CHECKLIST.md
    └── INSPECTION_TESTING_ROADMAP.md
```

---

## 👥 User Roles

### 🛒 Buyer

- Browse and search car listings
- View car details with inspection reports
- Request vehicle inspections
- Track inspection request status
- View completed inspection reports

### 🏪 Seller

- Post new car listings (requires admin approval)
- Edit/delete own listings
- Accept/reject inspection requests
- Schedule inspection appointments
- View inspection reports for own cars

### 🔧 Inspector

- View unassigned inspection requests
- Self-assign inspections
- Start inspections
- Submit detailed reports (14 components + photos)
- View submitted reports

### 👨‍💼 Admin

- **Ad Moderation**: Approve/decline car listings
- **User Management**: View, edit roles, delete users
- **Inspection Oversight**: View all inspections, reassign inspectors
- **Analytics**: Dashboard with statistics and charts
- **Listing Management**: Delete any listing
- **Full System Access**: Override permissions

---

## 📖 Usage Guide

### For Buyers

1. **Register/Login**:

   - Go to http://127.0.0.1:8000/users/register/
   - Select "Buyer" role
   - Fill in details and register

2. **Browse Cars**:

   - Click "Browse Cars" in navbar
   - Use search filters (make, model, price)
   - View car details

3. **Request Inspection**:
   - On car detail page, click "Request Inspection"
   - Track status in "My Requests" menu
   - View report when completed

### For Sellers

1. **Post a Listing**:

   - Login as seller
   - Click "Sell Car" in navbar
   - Fill in car details and upload images
   - Submit (goes to pending for admin approval)

2. **Manage Inspection Requests**:
   - Go to "Inspections" menu
   - Accept/reject requests
   - Schedule inspection date/time

### For Inspectors

1. **Assign Inspection**:

   - Go to "Inspector Dashboard"
   - View unassigned inspections
   - Click "Assign to Me"

2. **Submit Report**:
   - Start inspection
   - Rate 14 vehicle components (1-5)
   - Upload photos (up to 10)
   - Add comments
   - Submit report

### For Admins

1. **Access Admin Panel**:

   - Login with admin credentials
   - Click yellow "Admin Panel" link in navbar

2. **Moderate Ads**:

   - View "Pending Ads"
   - Approve or decline with reason

3. **Manage Users**:

   - View all users
   - Edit roles
   - Delete accounts

4. **Monitor Inspections**:
   - View all inspection requests
   - Filter by status
   - Reassign inspectors if needed

---

## 🎛️ Admin Panel

### Default Admin Credentials

- **URL**: http://127.0.0.1:8000/admin-panel/
- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Important**: Change default password after first login!

### Admin Features

#### Dashboard (`/admin-panel/`)

- User statistics (total, buyers, sellers, inspectors, online)
- Car statistics (total, pending, published, declined)
- Inspection statistics (total, completed, in-progress)
- Pie chart: Ads by city
- Bar chart: Ads by make
- Pending requests preview

#### Ad Moderation (`/admin-panel/pending-ads/`)

- Review all pending car listings
- Approve → Makes listing public
- Decline → Specify reason (visible to seller)

#### User Management (`/admin-panel/users/`)

- View all users with details
- Filter by role
- Edit user roles (including promoting to admin)
- Delete users (cannot delete own account)

#### Inspection Oversight (`/admin-panel/inspections/`)

- View all inspection requests
- Filter by status (7 statuses)
- Reassign inspectors
- View completed reports

#### All Listings (`/admin-panel/all-listings/`)

- View complete car inventory
- Filter by status
- Delete any listing

---

## 🔧 Troubleshooting

### Common Issues

#### "pip is not recognized"

**Solution**: Add Python to PATH during installation or run:

```powershell
python -m pip install -r requirements.txt
```

#### "Execution Policy Error" when activating virtual environment

**Solution**: Run PowerShell as Administrator:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### "Port 8000 already in use"

**Solution**: Kill existing process:

```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F
```

Or use a different port:

```powershell
python manage.py runserver 8080
```

#### "No module named 'PIL'"

**Solution**: Reinstall Pillow:

```powershell
pip uninstall Pillow
pip install Pillow
```

#### Database errors after git pull

**Solution**: Reset database:

```powershell
# Delete database (WARNING: loses all data)
Remove-Item db.sqlite3

# Recreate database
python manage.py migrate

# Recreate admin user
python create_admin.py
```

#### Images not displaying

**Solution**: Ensure media files are served in development:

1. Check `settings.py` has `MEDIA_URL` and `MEDIA_ROOT` configured
2. Media URLs are added in `urls.py`
3. Images are in `media/cars/` or `media/inspections/`

---

## 📚 Documentation

Comprehensive documentation is available in the project:

- **`ADMIN_ROLE_GUIDE.md`**: Complete admin feature documentation
- **`ADMIN_QUICKSTART.md`**: Quick start guide for admin panel
- **`ADMIN_TESTING_CHECKLIST.md`**: 45+ test cases for admin features
- **`INSPECTION_TESTING_ROADMAP.md`**: Complete testing guide for inspection system
- **`ADMIN_IMPLEMENTATION_SUMMARY.md`**: Implementation summary

---

## 🚀 Quick Start Commands

```powershell
# Clone project
git clone https://github.com/Bilal-Ayub/WheelDeals.git
cd WheelDeals

# Setup environment
python -m venv my_env
.\my_env\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create admin
python create_admin.py

# Run server
python manage.py runserver

# Access application
# Homepage: http://127.0.0.1:8000/
# Admin Panel: http://127.0.0.1:8000/admin-panel/
```

---

## 🧪 Testing

### Create Test Users (Optional)

```powershell
python manage.py shell
```

```python
from users.models import CustomUser

# Create Buyer
buyer = CustomUser.objects.create_user(
    username='buyer1', password='buyer123',
    email='buyer@test.com', role='buyer',
    first_name='John', last_name='Buyer'
)

# Create Seller
seller = CustomUser.objects.create_user(
    username='seller1', password='seller123',
    email='seller@test.com', role='seller',
    first_name='Jane', last_name='Seller'
)

# Create Inspector
inspector = CustomUser.objects.create_user(
    username='inspector1', password='inspector123',
    email='inspector@test.com', role='inspector',
    first_name='Mike', last_name='Inspector'
)

print("✓ Test users created!")
exit()
```

### Run Data Verification

```powershell
python verify_admin_data.py
```

### Manual Testing

Follow the testing roadmaps:

- `INSPECTION_TESTING_ROADMAP.md` - 18 test cases for inspections
- `ADMIN_TESTING_CHECKLIST.md` - 45+ test cases for admin features

---

## 🔐 Security Notes

### For Development

- ✅ Use default credentials for testing
- ✅ SQLite database is acceptable
- ✅ DEBUG = True is fine

### For Production

- ⚠️ **Change SECRET_KEY** in settings.py
- ⚠️ **Change default admin password**
- ⚠️ Set **DEBUG = False**
- ⚠️ Use **PostgreSQL/MySQL** instead of SQLite
- ⚠️ Configure **ALLOWED_HOSTS**
- ⚠️ Enable **HTTPS**
- ⚠️ Set up proper **media file serving** (AWS S3, etc.)
- ⚠️ Add **rate limiting** on sensitive endpoints
- ⚠️ Regular **database backups**

---

## 📊 Database Schema

### Key Models

**CustomUser**

- Extended Django User with roles (buyer, seller, inspector, admin)
- Custom fields: phone, city, is_guest

**Car**

- Fields: make, model, year, price, mileage, color, transmission, fuel_type
- Status: pending, published, declined
- Images: image1, image2, image3
- Tracking: views, viewed_by, date_posted

**InspectionRequest**

- Auto-generated ID (INS-YYYYMMDD-XXXXX)
- Status workflow: requested → accepted → assigned → in_progress → completed
- Links: buyer, seller, car, inspector
- Scheduling: scheduled_date, time_slot
- Payment: Fixed $50

**InspectionReport**

- 14 component ratings (1-5 scale)
- Components: paint, body, glass, lights, tires, wheels, engine, transmission, brakes, suspension, interior, seats, dashboard, electronics
- Overall comments
- Completion date
- Average rating calculation

**InspectionPhoto**

- Multiple photos per report (max 10)
- Image upload with captions

---

## SQL Queries Documentation

For detailed SQL queries used throughout the application, see the individual model files:

- `cars/models.py` - SQL documentation for car-related queries
- `users/models.py` - User authentication queries
- `inspections/models.py` - Inspection workflow queries

---

## ✅ Success Checklist

After installation, verify:

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list` shows Django, Pillow)
- [ ] Migrations applied (`python manage.py showmigrations`)
- [ ] Admin user created (can login at `/admin-panel/`)
- [ ] Server running at http://127.0.0.1:8000/
- [ ] Homepage loads correctly
- [ ] Can register new users
- [ ] Can create car listings (as seller)
- [ ] Admin panel accessible

---

## 🎓 Academic Context

**Course**: Database Systems (Fall 2025)  
**Project Type**: Django Web Application with SQLite  
**Features**:

- CRUD operations
- Role-based access control
- Complex workflows (inspection system)
- Admin panel with analytics
- Image upload and management
- Relational database design

---

## 📞 Support

If you encounter any issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review documentation files in the project
3. Verify Python version: `python --version` (should be 3.12+)
4. Ensure all migrations are applied: `python manage.py showmigrations`
5. Check console for error messages
6. Run data verification: `python verify_admin_data.py`

---

## 👤 Author

**Bilal Ayub**

- GitHub: [@Bilal-Ayub](https://github.com/Bilal-Ayub)
- Repository: [WheelDeals](https://github.com/Bilal-Ayub/WheelDeals)

---

## 🤝 Contributing

This is an academic project for database course (Fall 2025).

---

## 📄 License

This project is created for educational purposes as part of a university database course.

---

**🎉 You're all set! Happy coding!**

For questions or issues, refer to the documentation files or check the Django error messages in the terminal.

---

## 📝 Quick Reference

### Essential Commands

```powershell
# Activate environment
.\my_env\Scripts\Activate.ps1

# Run server
python manage.py runserver

# Make migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```

### Important URLs

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin-panel/
- **Django Admin**: http://127.0.0.1:8000/admin/
- **Login**: http://127.0.0.1:8000/users/login/
- **Register**: http://127.0.0.1:8000/users/register/
- **Browse Cars**: http://127.0.0.1:8000/cars/
- **Inspector Dashboard**: http://127.0.0.1:8000/inspections/inspector/dashboard/

### Default Credentials

| Role  | Username | Password   |
| ----- | -------- | ---------- |
| Admin | `admin`  | `admin123` |

---

**Last Updated**: December 1, 2025

# WheelDeals - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Navigate to Project

```bash
cd "C:\Users\Bilal A\Documents\Fall_2025\DB\project\wheeldeals"
```

### Step 2: Activate Virtual Environment

```powershell
# PowerShell
.\venv\Scripts\Activate.ps1

# Or Command Prompt
venv\Scripts\activate.bat
```

### Step 3: Verify Installation

```bash
python -m django --version
# Should show: 5.2.8
```

### Step 4: Create Admin User (First Time Only)

```bash
python manage.py createsuperuser
```

Follow prompts:

- Username: admin
- Email: admin@wheeldeals.com
- Password: (choose a password)

### Step 5: Run Server

```bash
python manage.py runserver
```

### Step 6: Open Browser

Visit: **http://localhost:8000/**

---

## 🎯 Quick Demo Workflow

### 1. Homepage

- URL: http://localhost:8000/
- Shows welcome screen and recent cars

### 2. Register New User

- Click "Sign Up" button
- Fill in form:
  - Username: `testuser`
  - First Name: `John`
  - Last Name: `Doe`
  - Email: `john@example.com`
  - Phone: `555-0123`
  - City: `New York`
  - Password: `testpass123`
  - Confirm Password: `testpass123`
- Click "Create Account"

### 3. Login

- Click "Login"
- Enter username and password
- Should redirect to homepage (now logged in)

### 4. Add a Car

- Click "Sell Car" in navbar
- Fill in form:
  - Make: `Toyota`
  - Model: `Camry`
  - Year: `2020`
  - Price: `25000`
  - Mileage: `30000`
  - Color: `Silver`
  - Transmission: `Automatic`
  - Fuel Type: `Petrol`
  - Description: `Well-maintained, single owner, excellent condition.`
  - Upload images (optional)
- Click "Save Listing"

### 5. Browse Cars

- Click "Browse Cars" in navbar
- See grid of all cars
- Use search box to search
- Apply filters (price, transmission, fuel type)
- Click on a car to view details

### 6. View Car Details

- Click "View Details" on any car
- See all specifications
- View seller information
- Click "Contact Seller" to email

### 7. Edit Profile

- Click "Profile" in navbar
- Update your information
- View your car listings
- Edit or delete your cars

### 8. Admin Panel

- URL: http://localhost:8000/admin/
- Login with superuser credentials
- Manage users and cars
- View all database entries

---

## 📊 Testing SQL Queries

### View SQL in Django Shell

```bash
python manage.py shell
```

```python
from cars.models import Car
from django.contrib.auth import get_user_model

User = get_user_model()

# Get all available cars
cars = Car.objects.filter(is_sold=False)
print(cars.query)  # Shows SQL query

# Get car with seller info
car = Car.objects.select_related('seller').first()
print(car.make, car.model, car.seller.username)

# Count cars
count = Car.objects.filter(is_sold=False).count()
print(f"Total available cars: {count}")
```

### View Actual SQL (Enable Debug)

In `settings.py`, ensure `DEBUG = True`, then:

```python
from django.db import connection
from cars.models import Car

# Execute a query
cars = list(Car.objects.all())

# View queries
for query in connection.queries:
    print(query['sql'])
```

---

## 🔍 Accessing Different Pages

| Feature     | URL                                   | Auth Required?  |
| ----------- | ------------------------------------- | --------------- |
| Home        | http://localhost:8000/                | No              |
| Browse Cars | http://localhost:8000/cars/           | No              |
| Car Detail  | http://localhost:8000/cars/1/         | No              |
| Add Car     | http://localhost:8000/cars/add/       | Yes             |
| Register    | http://localhost:8000/users/register/ | No              |
| Login       | http://localhost:8000/users/login/    | No              |
| Profile     | http://localhost:8000/users/profile/  | Yes             |
| Admin       | http://localhost:8000/admin/          | Yes (superuser) |

---

## 🗄️ Database Commands

### View Database Schema

```bash
python manage.py dbshell
```

```sql
.tables                    -- List all tables
.schema users_customuser   -- View user table schema
.schema cars_car          -- View car table schema
SELECT * FROM cars_car;   -- View all cars
SELECT * FROM users_customuser;  -- View all users
.quit                     -- Exit
```

### Reset Database (if needed)

```bash
# Delete database
del db.sqlite3

# Delete migrations
del cars\migrations\0*.py
del users\migrations\0*.py

# Recreate
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## 📸 Adding Sample Data

### Via Admin Panel

1. Go to http://localhost:8000/admin/
2. Login with superuser account
3. Click "Cars" → "Add Car"
4. Fill in details and save

### Via Django Shell

```bash
python manage.py shell
```

```python
from cars.models import Car
from django.contrib.auth import get_user_model

User = get_user_model()

# Get a user (or create one)
user = User.objects.first()

# Create sample cars
Car.objects.create(
    make="Honda",
    model="Civic",
    year=2021,
    price=22000,
    mileage=15000,
    color="Blue",
    transmission="automatic",
    fuel_type="petrol",
    description="Like new, low mileage",
    seller=user
)

Car.objects.create(
    make="Ford",
    model="Mustang",
    year=2019,
    price=35000,
    mileage=25000,
    color="Red",
    transmission="manual",
    fuel_type="petrol",
    description="Sports car, excellent condition",
    seller=user
)

print("Sample cars created!")
```

---

## 🐛 Troubleshooting

### Problem: Port already in use

```bash
# Use different port
python manage.py runserver 8080
```

### Problem: Static files not loading

```bash
python manage.py collectstatic --noinput
```

### Problem: Database locked

- Close all database connections
- Restart server

### Problem: Module not found

```bash
# Ensure virtual environment is activated
# Then reinstall
pip install -r requirements.txt
```

---

## 📝 Key Files to Know

- **`manage.py`** - Run Django commands
- **`db.sqlite3`** - Database file
- **`settings.py`** - Project configuration
- **`urls.py`** - URL routing
- **`models.py`** - Database models
- **`views.py`** - View logic
- **`templates/`** - HTML files
- **`static/`** - CSS, JS, images
- **`media/`** - User uploads

---

## 🎓 Learning Resources

### Django ORM vs SQL

Every Django ORM query translates to SQL. Examples:

```python
# Django ORM
Car.objects.filter(make="Toyota")

# Equivalent SQL
SELECT * FROM cars_car WHERE make = 'Toyota';
```

```python
# Django ORM
Car.objects.filter(price__gte=20000, price__lte=30000)

# Equivalent SQL
SELECT * FROM cars_car WHERE price >= 20000 AND price <= 30000;
```

See `SQL_QUERIES.md` for all queries used in this project.

---

## ✅ Checklist Before Demo

- [ ] Database exists (db.sqlite3)
- [ ] Superuser created
- [ ] At least 3-5 sample cars added
- [ ] Server running without errors
- [ ] Can access http://localhost:8000/
- [ ] Can login to admin panel
- [ ] Can register new user
- [ ] Can add new car
- [ ] Images upload working
- [ ] All links work
- [ ] SQL_QUERIES.md reviewed

---

## 🚀 Ready to Present!

Your WheelDeals project is now ready to demonstrate. You have:

✅ 6 functional screens (50% requirement)
✅ SQL queries documented for each screen
✅ Working authentication system
✅ CRUD operations for cars
✅ Beautiful Bootstrap UI
✅ Responsive design
✅ Database with proper relationships

**Good luck with your presentation! 🎉**

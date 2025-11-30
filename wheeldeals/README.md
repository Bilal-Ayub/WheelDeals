# WheelDeals - Car Buying & Selling Platform

## Project Overview

WheelDeals is a Django-based web application for buying and selling cars. Users can browse car listings, post their own vehicles for sale, and manage their profiles.

## Database Structure

### Tables Created:

1. **users_customuser** - User accounts

   - Fields: id, username, email, password, first_name, last_name, phone, city
   - Primary Key: id

2. **cars_car** - Vehicle listings
   - Fields: id, make, model, year, price, mileage, color, transmission, fuel_type, description, image1, image2, image3, seller_id, date_posted, is_sold, views
   - Primary Key: id
   - Foreign Key: seller_id → users_customuser(id)

## SQL Queries for Each Screen

### 1. Home Page

```sql
-- Get all available cars (not sold)
SELECT * FROM cars_car
WHERE is_sold = 0
ORDER BY date_posted DESC
LIMIT 10;
```

### 2. User Registration

```sql
-- Insert new user
INSERT INTO users_customuser (
    username, email, password, first_name, last_name, phone, city,
    is_staff, is_active, is_superuser, date_joined
) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 1, 0, CURRENT_TIMESTAMP);
```

### 3. User Login

```sql
-- Authenticate user
SELECT id, username, password, email, first_name, last_name
FROM users_customuser
WHERE username = ? AND is_active = 1;
```

### 4. Car Listings (Browse All Cars)

```sql
-- Get all cars with pagination
SELECT c.*, u.username as seller_name, u.phone as seller_phone
FROM cars_car c
JOIN users_customuser u ON c.seller_id = u.id
WHERE c.is_sold = 0
ORDER BY c.date_posted DESC
LIMIT 12 OFFSET ?;

-- Count total cars for pagination
SELECT COUNT(*) FROM cars_car WHERE is_sold = 0;
```

### 5. Car Detail Page

```sql
-- Get specific car with seller details
SELECT c.*,
       u.username, u.email, u.phone, u.city
FROM cars_car c
JOIN users_customuser u ON c.seller_id = u.id
WHERE c.id = ?;

-- Update view count
UPDATE cars_car
SET views = views + 1
WHERE id = ?;
```

### 6. Add/Post Car

```sql
-- Insert new car listing
INSERT INTO cars_car (
    make, model, year, price, mileage, color, transmission,
    fuel_type, description, image1, image2, image3,
    seller_id, date_posted, is_sold, views
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, 0, 0);
```

### 7. Edit User Profile

```sql
-- Get user details
SELECT * FROM users_customuser WHERE id = ?;

-- Update user profile
UPDATE users_customuser
SET first_name = ?, last_name = ?, email = ?, phone = ?, city = ?
WHERE id = ?;
```

### Additional Queries

#### Search Cars

```sql
-- Search by make, model, or year
SELECT c.*, u.username as seller_name
FROM cars_car c
JOIN users_customuser u ON c.seller_id = u.id
WHERE (c.make LIKE '%?%' OR c.model LIKE '%?%' OR c.year = ?)
  AND c.is_sold = 0
ORDER BY c.date_posted DESC;
```

#### Filter by Price Range

```sql
SELECT c.*, u.username as seller_name
FROM cars_car c
JOIN users_customuser u ON c.seller_id = u.id
WHERE c.price BETWEEN ? AND ?
  AND c.is_sold = 0
ORDER BY c.price ASC;
```

#### Get User's Cars

```sql
-- Get all cars posted by a specific user
SELECT * FROM cars_car
WHERE seller_id = ?
ORDER BY date_posted DESC;
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

### 5. Access the Application

- Main site: http://localhost:8000/
- Admin panel: http://localhost:8000/admin/

## Project Structure

```
wheeldeals/
├── cars/                   # Cars app
│   ├── models.py          # Car model
│   ├── views.py           # Views for car listings
│   ├── forms.py           # Forms for adding cars
│   ├── urls.py            # URL routing for cars
│   └── admin.py           # Admin configuration
├── users/                  # Users app
│   ├── models.py          # Custom User model
│   ├── views.py           # Views for auth
│   ├── forms.py           # Registration/login forms
│   └── admin.py           # Admin configuration
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Home page
│   ├── cars/              # Car-related templates
│   └── users/             # User-related templates
├── static/                 # Static files (CSS, JS, Images)
│   ├── css/
│   ├── js/
│   └── images/
├── media/                  # User uploads (car images)
├── wheeldeals_project/     # Project settings
│   ├── settings.py        # Configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI config
└── manage.py              # Django management script
```

## Features Implemented (50% - 6 screens)

1. ✅ **Home/Landing Page** - Welcome and featured cars
2. ✅ **User Registration** - Sign up new users
3. ✅ **User Login** - Authenticate users
4. ✅ **Car Listings** - Browse all available cars
5. ✅ **Car Detail** - View detailed car information
6. ✅ **Add Car** - Post new car for sale

## Technologies Used

- **Backend**: Django 5.2.8
- **Database**: SQLite (development)
- **Frontend**: HTML, CSS (Bootstrap 5), JavaScript
- **Image Processing**: Pillow

## Database Models Explanation

### CustomUser Model

Extends Django's built-in User model with additional fields:

- `phone`: Contact number
- `city`: User's location

### Car Model

Stores vehicle listing information:

- **Basic Info**: make, model, year, price
- **Specs**: mileage, color, transmission, fuel_type
- **Media**: up to 3 images
- **Metadata**: seller (FK to User), date_posted, is_sold, views

## Next Steps

- Implement remaining 6 screens (search, filters, user dashboard, etc.)
- Add image upload functionality
- Implement search and filter features
- Add user authentication protection
- Style with Bootstrap 5 matching the UI mockups

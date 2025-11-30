# WheelDeals Project Summary

## Project Completion Status: 50% (6 of 12 screens implemented)

---

## Implemented Screens

### ✅ 1. Home/Landing Page (`/`)

- **Template**: `templates/home.html`
- **View**: `cars.views.home`
- **Features**:
  - Hero section with call-to-action
  - Statistics display (total cars available)
  - Recent 8 car listings
  - "How It Works" section
  - Responsive design with Bootstrap 5

**SQL Queries Used**:

```sql
-- Get recent cars
SELECT * FROM cars_car WHERE is_sold = 0 ORDER BY date_posted DESC LIMIT 8;

-- Count total available cars
SELECT COUNT(*) FROM cars_car WHERE is_sold = 0;
```

---

### ✅ 2. User Registration (`/users/register/`)

- **Template**: `templates/users/register.html`
- **View**: `users.views.register`
- **Form**: `CustomUserCreationForm`
- **Features**:
  - Username, email, password fields
  - Additional fields: first_name, last_name, phone, city
  - Password confirmation
  - Form validation
  - Redirect to login after successful registration

**SQL Query Used**:

```sql
INSERT INTO users_customuser (
    username, email, password, first_name, last_name, phone, city,
    is_staff, is_active, is_superuser, date_joined
) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 1, 0, CURRENT_TIMESTAMP);
```

---

### ✅ 3. User Login (`/users/login/`)

- **Template**: `templates/users/login.html`
- **View**: `users.views.user_login`
- **Form**: Django's `AuthenticationForm`
- **Features**:
  - Username and password authentication
  - Session management
  - Redirect to home after login
  - Error messages for invalid credentials

**SQL Queries Used**:

```sql
-- Authenticate user
SELECT id, username, password, email, first_name, last_name
FROM users_customuser
WHERE username = ? AND is_active = 1;

-- Update last login
UPDATE users_customuser SET last_login = CURRENT_TIMESTAMP WHERE id = ?;
```

---

### ✅ 4. Car Listings / Browse Cars (`/cars/`)

- **Template**: `templates/cars/car_list.html`
- **View**: `cars.views.car_list`
- **Form**: `CarSearchForm`
- **Features**:
  - Grid display of all available cars (12 per page)
  - Search by make, model, description
  - Filter by price range, transmission, fuel type
  - Pagination
  - Car cards showing image, make, model, year, price, specs
  - View count display

**SQL Queries Used**:

```sql
-- Get all cars with seller info (paginated)
SELECT c.*, u.username as seller_name, u.phone as seller_phone
FROM cars_car c
JOIN users_customuser u ON c.seller_id = u.id
WHERE c.is_sold = 0
ORDER BY c.date_posted DESC
LIMIT 12 OFFSET ?;

-- Search by make/model
SELECT * FROM cars_car
WHERE (make LIKE '%?%' OR model LIKE '%?%' OR description LIKE '%?%')
AND is_sold = 0
ORDER BY date_posted DESC;

-- Filter by price range
SELECT * FROM cars_car
WHERE price BETWEEN ? AND ? AND is_sold = 0
ORDER BY price ASC;

-- Count for pagination
SELECT COUNT(*) FROM cars_car WHERE is_sold = 0;
```

---

### ✅ 5. Car Detail Page (`/cars/<id>/`)

- **Template**: `templates/cars/car_detail.html`
- **View**: `cars.views.car_detail`
- **Features**:
  - Image carousel (up to 3 images)
  - Complete car specifications
  - Seller information (name, email, phone, city)
  - Contact seller button (mailto link)
  - View counter (auto-increments)
  - Related cars (same make)
  - Edit/Delete buttons (for car owner only)

**SQL Queries Used**:

```sql
-- Get car with seller details
SELECT c.*, u.username, u.email, u.phone, u.city
FROM cars_car c
JOIN users_customuser u ON c.seller_id = u.id
WHERE c.id = ?;

-- Increment view count
UPDATE cars_car SET views = views + 1 WHERE id = ?;

-- Get related cars
SELECT * FROM cars_car
WHERE make = ? AND id != ? AND is_sold = 0
LIMIT 4;
```

---

### ✅ 6. Add/Post Car (`/cars/add/`)

- **Template**: `templates/cars/car_form.html`
- **View**: `cars.views.car_create`
- **Form**: `CarForm`
- **Features**:
  - Requires authentication (`@login_required`)
  - Fields: make, model, year, price, mileage, color, transmission, fuel_type, description
  - Image upload (up to 3 images)
  - Form validation
  - Auto-assigns logged-in user as seller
  - Redirects to car detail page after creation

**SQL Query Used**:

```sql
INSERT INTO cars_car (
    make, model, year, price, mileage, color, transmission,
    fuel_type, description, image1, image2, image3,
    seller_id, date_posted, is_sold, views
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, 0, 0);
```

---

### ✅ Bonus Screen: User Profile (`/users/profile/`)

- **Template**: `templates/users/profile.html`
- **View**: `users.views.profile`
- **Form**: `CustomUserUpdateForm`
- **Features**:
  - Edit user details (first_name, last_name, email, phone, city)
  - View all user's car listings
  - Table showing car title, price, status, views
  - Quick actions (View, Edit, Delete) for each car
  - Link to add new car

**SQL Queries Used**:

```sql
-- Get user data
SELECT * FROM users_customuser WHERE id = ?;

-- Update user profile
UPDATE users_customuser
SET first_name = ?, last_name = ?, email = ?, phone = ?, city = ?
WHERE id = ?;

-- Get user's cars
SELECT * FROM cars_car WHERE seller_id = ? ORDER BY date_posted DESC;
```

---

## Database Schema

### Table 1: users_customuser

| Column       | Type         | Constraints               |
| ------------ | ------------ | ------------------------- |
| id           | INTEGER      | PRIMARY KEY AUTOINCREMENT |
| username     | VARCHAR(150) | UNIQUE NOT NULL           |
| email        | VARCHAR(254) | NOT NULL                  |
| password     | VARCHAR(128) | NOT NULL                  |
| first_name   | VARCHAR(150) | NOT NULL                  |
| last_name    | VARCHAR(150) | NOT NULL                  |
| phone        | VARCHAR(15)  | NULL                      |
| city         | VARCHAR(100) | NULL                      |
| is_staff     | BOOL         | NOT NULL                  |
| is_active    | BOOL         | NOT NULL                  |
| is_superuser | BOOL         | NOT NULL                  |
| date_joined  | DATETIME     | NOT NULL                  |
| last_login   | DATETIME     | NULL                      |

### Table 2: cars_car

| Column       | Type          | Constraints                        |
| ------------ | ------------- | ---------------------------------- |
| id           | INTEGER       | PRIMARY KEY AUTOINCREMENT          |
| make         | VARCHAR(100)  | NOT NULL                           |
| model        | VARCHAR(100)  | NOT NULL                           |
| year         | INTEGER       | NOT NULL                           |
| price        | DECIMAL(10,2) | NOT NULL                           |
| mileage      | INTEGER       | NULL                               |
| color        | VARCHAR(50)   | NULL                               |
| transmission | VARCHAR(20)   | NOT NULL                           |
| fuel_type    | VARCHAR(20)   | NOT NULL                           |
| description  | TEXT          | NULL                               |
| image1       | VARCHAR(100)  | NULL                               |
| image2       | VARCHAR(100)  | NULL                               |
| image3       | VARCHAR(100)  | NULL                               |
| seller_id    | INTEGER       | FOREIGN KEY → users_customuser(id) |
| date_posted  | DATETIME      | NOT NULL                           |
| is_sold      | BOOL          | NOT NULL DEFAULT 0                 |
| views        | INTEGER       | NOT NULL DEFAULT 0                 |

---

## Project Structure

```
wheeldeals/
├── cars/                          # Cars application
│   ├── admin.py                   # Admin configuration
│   ├── forms.py                   # CarForm, CarSearchForm
│   ├── models.py                  # Car model
│   ├── urls.py                    # URL patterns
│   └── views.py                   # Views (home, car_list, car_detail, car_create, car_update, car_delete)
│
├── users/                         # Users application
│   ├── admin.py                   # Admin configuration
│   ├── forms.py                   # CustomUserCreationForm, CustomUserUpdateForm
│   ├── models.py                  # CustomUser model
│   ├── urls.py                    # URL patterns
│   └── views.py                   # Views (register, login, logout, profile)
│
├── templates/                     # HTML templates
│   ├── base.html                  # Base template with navbar, footer
│   ├── home.html                  # Landing page
│   ├── cars/
│   │   ├── car_list.html         # Browse cars page
│   │   ├── car_detail.html       # Car detail page
│   │   ├── car_form.html         # Add/Edit car form
│   │   └── car_confirm_delete.html  # Delete confirmation
│   └── users/
│       ├── register.html          # Registration form
│       ├── login.html             # Login form
│       └── profile.html           # User profile & edit
│
├── static/                        # Static files
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                         # User uploads (car images)
│
├── wheeldeals_project/           # Project settings
│   ├── settings.py               # Configuration
│   ├── urls.py                   # Main URL routing
│   └── wsgi.py                   # WSGI configuration
│
├── db.sqlite3                    # SQLite database
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
└── SQL_QUERIES.md               # SQL queries documentation
```

---

## Technologies Used

- **Backend**: Django 5.2.8
- **Database**: SQLite3 (development)
- **Frontend**: HTML5, CSS3, Bootstrap 5.3
- **JavaScript**: Bootstrap JS (for modals, carousels, etc.)
- **Icons**: Font Awesome 6.4
- **Image Processing**: Pillow 12.0.0
- **Python**: 3.12.7

---

## How to Run the Project

### 1. Navigate to Project Directory

```bash
cd wheeldeals
```

### 2. Activate Virtual Environment

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies (if not already installed)

```bash
pip install -r requirements.txt
```

### 4. Run Migrations (if not already done)

```bash
python manage.py migrate
```

### 5. Create Superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

### 7. Access the Application

- **Main Website**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **Browse Cars**: http://localhost:8000/cars/
- **Register**: http://localhost:8000/users/register/
- **Login**: http://localhost:8000/users/login/

---

## URL Patterns

| URL                  | View          | Description                   |
| -------------------- | ------------- | ----------------------------- |
| `/`                  | `home`        | Landing page                  |
| `/cars/`             | `car_list`    | Browse all cars               |
| `/cars/<id>/`        | `car_detail`  | Car detail page               |
| `/cars/add/`         | `car_create`  | Add new car (requires login)  |
| `/cars/<id>/edit/`   | `car_update`  | Edit car (owner only)         |
| `/cars/<id>/delete/` | `car_delete`  | Delete car (owner only)       |
| `/users/register/`   | `register`    | User registration             |
| `/users/login/`      | `user_login`  | User login                    |
| `/users/logout/`     | `user_logout` | User logout                   |
| `/users/profile/`    | `profile`     | User profile (requires login) |
| `/admin/`            | Django Admin  | Admin panel                   |

---

## Features Implemented

✅ User authentication (register, login, logout)
✅ Custom user model with additional fields
✅ Car listings with pagination
✅ Search and filter functionality
✅ Car detail view with image carousel
✅ Add new car listing (with image upload)
✅ Edit car listing (owner only)
✅ Delete car listing (owner only)
✅ User profile management
✅ View counter for car listings
✅ Related cars suggestion
✅ Responsive design (mobile-friendly)
✅ Form validation
✅ Error handling and user feedback (messages)
✅ Admin panel configuration

---

## Remaining Screens (for 100% completion)

The following screens could be implemented to complete the full 12 screens:

1. **Advanced Search Page** - Dedicated search page with more filters
2. **My Favorites/Watchlist** - Users can save cars they're interested in
3. **Car Comparison** - Compare multiple cars side by side
4. **User Dashboard** - Analytics for sellers (views, inquiries, etc.)
5. **Messages/Inbox** - Internal messaging between buyers and sellers
6. **Transaction History** - Record of sold cars

---

## SQL Queries Summary

Total unique SQL queries documented: **25+**

Key query types:

- SELECT (with JOIN, WHERE, ORDER BY, LIMIT)
- INSERT
- UPDATE
- DELETE
- COUNT/Aggregate functions
- Full-text search (LIKE)
- Price range filters
- Pagination (LIMIT/OFFSET)

All queries are documented in `SQL_QUERIES.md`.

---

## Testing the Application

### Test Workflow:

1. **Start Server**: `python manage.py runserver`
2. **Visit Home Page**: http://localhost:8000/
3. **Register New User**: Click "Sign Up" → Fill form → Submit
4. **Login**: Use credentials → Access protected features
5. **Add Car**: Click "Sell Car" → Fill form → Upload images → Submit
6. **Browse Cars**: Click "Browse Cars" → Search/Filter → View details
7. **Edit Profile**: Click "Profile" → Update information → Save
8. **View Car Details**: Click on any car → See full information
9. **Test Admin**: http://localhost:8000/admin/ → Manage users/cars

---

## Project Deliverables Checklist

✅ Django project setup
✅ Database models (User, Car)
✅ 6 functional screens (50% requirement met)
✅ SQL queries documented for each screen
✅ Bootstrap UI matching mockups
✅ Image upload functionality
✅ User authentication
✅ CRUD operations (Create, Read, Update, Delete)
✅ Search and filter features
✅ Responsive design
✅ README documentation
✅ SQL_QUERIES.md documentation

---

## Notes for Demonstration

- Database is SQLite (easy to demo, no setup required)
- All passwords are hashed using Django's authentication system
- Images are stored in `media/cars/` directory
- Static files use CDN (Bootstrap, Font Awesome) for quick loading
- The project follows Django best practices (MTV pattern, DRY principle)
- All forms include CSRF protection
- SQL queries can be viewed in Django Debug Toolbar (optional to install)

---

## Conclusion

The WheelDeals project successfully implements 50% of the required functionality with 6 fully functional screens. Each screen has corresponding SQL queries documented, and the application provides a complete user experience for car buying and selling. The project is ready for demonstration and can be easily extended with the remaining 6 screens.

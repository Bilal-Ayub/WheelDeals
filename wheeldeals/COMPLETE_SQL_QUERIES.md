# Complete SQL Queries by Screen - WheelDeals

This document contains **all SQL queries** for each screen in the WheelDeals application, organized by screen number with complete database schema.

---

## 📊 DATABASE SCHEMA

### Table 1: users_customuser

```sql
CREATE TABLE users_customuser (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME,
    is_superuser BOOL NOT NULL DEFAULT 0,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOL NOT NULL DEFAULT 0,
    is_active BOOL NOT NULL DEFAULT 1,
    date_joined DATETIME NOT NULL,
    phone VARCHAR(15),
    city VARCHAR(100),
    is_guest BOOL NOT NULL DEFAULT 0,
    role VARCHAR(10) NOT NULL DEFAULT 'buyer'
);

-- Indexes
CREATE INDEX idx_users_username ON users_customuser(username);
CREATE INDEX idx_users_email ON users_customuser(email);
CREATE INDEX idx_users_role ON users_customuser(role);
CREATE INDEX idx_users_is_guest ON users_customuser(is_guest);
```

### Table 2: cars_car

```sql
CREATE TABLE cars_car (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    mileage INTEGER,
    color VARCHAR(50),
    transmission VARCHAR(20) NOT NULL DEFAULT 'automatic',
    fuel_type VARCHAR(20) NOT NULL DEFAULT 'petrol',
    description TEXT,
    image1 VARCHAR(100),
    image2 VARCHAR(100),
    image3 VARCHAR(100),
    seller_id INTEGER NOT NULL,
    date_posted DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_sold BOOL NOT NULL DEFAULT 0,
    views INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (seller_id) REFERENCES users_customuser(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_cars_seller ON cars_car(seller_id);
CREATE INDEX idx_cars_make ON cars_car(make);
CREATE INDEX idx_cars_price ON cars_car(price);
CREATE INDEX idx_cars_is_sold ON cars_car(is_sold);
CREATE INDEX idx_cars_date_posted ON cars_car(date_posted DESC);
CREATE INDEX idx_cars_transmission ON cars_car(transmission);
CREATE INDEX idx_cars_fuel_type ON cars_car(fuel_type);
```

### Table 3: cars_car_viewed_by (Many-to-Many for unique view tracking)

```sql
CREATE TABLE cars_car_viewed_by (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER NOT NULL,
    customuser_id INTEGER NOT NULL,
    FOREIGN KEY (car_id) REFERENCES cars_car(id) ON DELETE CASCADE,
    FOREIGN KEY (customuser_id) REFERENCES users_customuser(id) ON DELETE CASCADE,
    UNIQUE(car_id, customuser_id)
);

-- Indexes
CREATE INDEX idx_viewed_car ON cars_car_viewed_by(car_id);
CREATE INDEX idx_viewed_user ON cars_car_viewed_by(customuser_id);
```

---

## 🏠 SCREEN 1: HOME PAGE (`/`)

**Purpose**: Landing page showing featured cars and registration options

### Query 1.1: Get Recent 8 Cars

```sql
SELECT
    id, make, model, year, price, mileage,
    fuel_type, image1, views, date_posted
FROM cars_car
WHERE is_sold = 0
ORDER BY date_posted DESC
LIMIT 8;
```

### Query 1.2: Count Available Cars (for stats)

```sql
SELECT COUNT(*) as total_cars
FROM cars_car
WHERE is_sold = 0;
```

**Returns**: Homepage displays recent listings + total count

---

## 📝 SCREEN 2: REGISTRATION (`/users/register/`)

**Purpose**: New user sign-up with role selection (Buyer/Seller)

### Query 2.1: Check Username Uniqueness

```sql
SELECT COUNT(*) as count
FROM users_customuser
WHERE username = ?;
```

**Expected**: count = 0 (available)

### Query 2.2: Check Email Uniqueness

```sql
SELECT COUNT(*) as count
FROM users_customuser
WHERE email = ?;
```

**Expected**: count = 0 (available)

### Query 2.3: Insert New User

```sql
INSERT INTO users_customuser (
    username, email, password, first_name, last_name,
    phone, city, role, is_guest, is_staff, is_active,
    is_superuser, date_joined
) VALUES (
    ?, ?, ?, ?, ?,
    ?, ?, ?, 0, 0, 1,
    0, CURRENT_TIMESTAMP
);
```

**Parameters**: username, email, hashed_password, first_name, last_name, phone, city, role ('buyer' or 'seller')

---

## 🔐 SCREEN 3: LOGIN (`/users/login/`)

**Purpose**: User authentication

### Query 3.1: Get User for Authentication

```sql
SELECT
    id, username, password, email, first_name, last_name,
    phone, city, role, is_guest, is_active
FROM users_customuser
WHERE username = ? AND is_active = 1;
```

**Parameters**: username

### Query 3.2: Update Last Login

```sql
UPDATE users_customuser
SET last_login = CURRENT_TIMESTAMP
WHERE id = ?;
```

**Parameters**: user_id

---

## 🚗 SCREEN 4: BROWSE CARS (`/cars/`)

**Purpose**: Search, filter, and browse all car listings

### Query 4.1: Base Query - All Cars (with Pagination)

```sql
SELECT
    c.id, c.make, c.model, c.year, c.price, c.mileage,
    c.color, c.transmission, c.fuel_type, c.image1,
    c.views, c.date_posted, c.is_sold,
    u.id as seller_id,
    u.username as seller_username,
    u.first_name as seller_first_name,
    u.last_name as seller_last_name,
    u.phone as seller_phone,
    u.city as seller_city,
    u.role as seller_role
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE c.is_sold = 0
ORDER BY c.date_posted DESC
LIMIT 12 OFFSET ?;
```

**Parameters**: offset (page_number \* 12)
**Returns**: 12 cars per page

### Query 4.2: Count Total (Pagination)

```sql
SELECT COUNT(*) as total
FROM cars_car
WHERE is_sold = 0;
```

### Query 4.3: Search by Text

```sql
SELECT c.*, u.username as seller_name, u.role as seller_role
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE (c.make LIKE ? OR c.model LIKE ? OR c.description LIKE ?)
  AND c.is_sold = 0
ORDER BY c.date_posted DESC;
```

**Parameters**: '%search%', '%search%', '%search%'

### Query 4.4: Filter by Price Range

```sql
SELECT c.*, u.username as seller_name
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE c.price >= ? AND c.price <= ?
  AND c.is_sold = 0
ORDER BY c.price ASC;
```

**Parameters**: min_price, max_price

### Query 4.5: Filter by Transmission

```sql
SELECT c.*, u.username as seller_name
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE c.transmission = ?
  AND c.is_sold = 0
ORDER BY c.date_posted DESC;
```

**Parameters**: 'automatic' OR 'manual'

### Query 4.6: Filter by Fuel Type

```sql
SELECT c.*, u.username as seller_name
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE c.fuel_type = ?
  AND c.is_sold = 0
ORDER BY c.date_posted DESC;
```

**Parameters**: 'petrol', 'diesel', 'electric', OR 'hybrid'

### Query 4.7: Combined Filters

```sql
SELECT c.*, u.username as seller_name
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE (c.make LIKE ? OR c.model LIKE ? OR c.description LIKE ?)
  AND c.price >= ? AND c.price <= ?
  AND c.transmission = ?
  AND c.fuel_type = ?
  AND c.is_sold = 0
ORDER BY c.date_posted DESC
LIMIT 12 OFFSET ?;
```

**Parameters**: search_text (3x), min_price, max_price, transmission, fuel_type, offset

---

## 🔍 SCREEN 5: CAR DETAIL (`/cars/<id>/`)

**Purpose**: View complete car details with seller contact info

### Query 5.1: Get Car with Seller Info

```sql
SELECT
    c.id, c.make, c.model, c.year, c.price, c.mileage,
    c.color, c.transmission, c.fuel_type, c.description,
    c.image1, c.image2, c.image3, c.date_posted, c.is_sold, c.views,
    u.id as seller_id,
    u.username as seller_username,
    u.first_name as seller_first_name,
    u.last_name as seller_last_name,
    u.email as seller_email,
    u.phone as seller_phone,
    u.city as seller_city,
    u.role as seller_role
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE c.id = ?;
```

**Parameters**: car_id

### Query 5.2: Check if User Already Viewed

```sql
SELECT COUNT(*) as has_viewed
FROM cars_car_viewed_by
WHERE car_id = ? AND customuser_id = ?;
```

**Parameters**: car_id, user_id
**Returns**: 0 (not viewed) or 1 (already viewed)

### Query 5.3: Record Unique View

```sql
INSERT INTO cars_car_viewed_by (car_id, customuser_id)
VALUES (?, ?);
```

**Parameters**: car_id, user_id
**Note**: Only executed if Query 5.2 returns 0

### Query 5.4: Increment View Count

```sql
UPDATE cars_car
SET views = views + 1
WHERE id = ?;
```

**Parameters**: car_id
**Note**: Only if new unique viewer

### Query 5.5: Get Related Cars (Same Make)

```sql
SELECT id, make, model, year, price, image1, is_sold
FROM cars_car
WHERE make = ?
  AND id != ?
  AND is_sold = 0
ORDER BY date_posted DESC
LIMIT 4;
```

**Parameters**: car_make, current_car_id

### Query 5.6: Get Unique Viewer Count

```sql
SELECT COUNT(DISTINCT customuser_id) as unique_viewers
FROM cars_car_viewed_by
WHERE car_id = ?;
```

**Parameters**: car_id

---

## 👤 SCREEN 6: USER PROFILE (`/users/profile/`)

**Purpose**: View/edit profile + manage car listings (sellers only)

### Query 6.1: Get User Profile

```sql
SELECT
    id, username, first_name, last_name, email,
    phone, city, role, is_guest, date_joined
FROM users_customuser
WHERE id = ?;
```

**Parameters**: user_id

### Query 6.2: Update Profile

```sql
UPDATE users_customuser
SET
    first_name = ?,
    last_name = ?,
    email = ?,
    phone = ?,
    city = ?
WHERE id = ?;
```

**Parameters**: first_name, last_name, email, phone, city, user_id

### Query 6.3: Get User's Car Listings (Sellers Only)

```sql
SELECT
    id, make, model, year, price, is_sold, views, date_posted
FROM cars_car
WHERE seller_id = ?
ORDER BY date_posted DESC;
```

**Parameters**: seller_user_id

### Query 6.4: Get Seller Statistics

```sql
SELECT
    COUNT(*) as total_listings,
    SUM(CASE WHEN is_sold = 1 THEN 1 ELSE 0 END) as sold_count,
    SUM(CASE WHEN is_sold = 0 THEN 1 ELSE 0 END) as active_count,
    SUM(views) as total_views,
    AVG(views) as avg_views
FROM cars_car
WHERE seller_id = ?;
```

**Parameters**: seller_user_id

---

## ➕ SCREEN 7: POST CAR (`/cars/add/`) - SELLERS ONLY

**Purpose**: Create new car listing

### Query 7.1: Verify User is Seller

```sql
SELECT role
FROM users_customuser
WHERE id = ? AND role = 'seller' AND is_guest = 0;
```

**Parameters**: user_id
**Expected**: Returns 'seller' or NULL (unauthorized)

### Query 7.2: Insert New Car

```sql
INSERT INTO cars_car (
    make, model, year, price, mileage, color,
    transmission, fuel_type, description,
    image1, image2, image3, seller_id,
    date_posted, is_sold, views
) VALUES (
    ?, ?, ?, ?, ?, ?,
    ?, ?, ?,
    ?, ?, ?, ?,
    CURRENT_TIMESTAMP, 0, 0
);
```

**Parameters**: make, model, year, price, mileage, color, transmission, fuel_type, description, image1, image2, image3, seller_id

---

## ✏️ SCREEN 8: EDIT CAR (`/cars/<id>/edit/`) - OWNER ONLY

**Purpose**: Edit existing car listing

### Query 8.1: Verify Ownership

```sql
SELECT *
FROM cars_car
WHERE id = ? AND seller_id = ?;
```

**Parameters**: car_id, user_id
**Returns**: Car data if owned, NULL otherwise

### Query 8.2: Update Car

```sql
UPDATE cars_car
SET
    make = ?, model = ?, year = ?, price = ?,
    mileage = ?, color = ?, transmission = ?,
    fuel_type = ?, description = ?,
    image1 = COALESCE(?, image1),
    image2 = COALESCE(?, image2),
    image3 = COALESCE(?, image3)
WHERE id = ? AND seller_id = ?;
```

**Parameters**: make, model, year, price, mileage, color, transmission, fuel_type, description, new_image1, new_image2, new_image3, car_id, seller_id
**Note**: Images only updated if new ones provided (COALESCE)

---

## 🗑️ SCREEN 9: DELETE CAR (`/cars/<id>/delete/`) - OWNER ONLY

**Purpose**: Delete car listing

### Query 9.1: Verify Ownership for Deletion

```sql
SELECT id, make, model, year, seller_id
FROM cars_car
WHERE id = ? AND seller_id = ?;
```

**Parameters**: car_id, user_id

### Query 9.2: Delete Car

```sql
DELETE FROM cars_car
WHERE id = ? AND seller_id = ?;
```

**Parameters**: car_id, seller_id

### Query 9.3: Cascade - Delete View Tracking

```sql
-- Automatically handled by CASCADE constraint
DELETE FROM cars_car_viewed_by
WHERE car_id = ?;
```

**Note**: Executed automatically by database

---

## 👻 SCREEN 10: GUEST MODE (`/users/guest/`)

**Purpose**: Create temporary guest user for browsing

### Query 10.1: Create Guest User

```sql
INSERT INTO users_customuser (
    username, password, is_guest, role,
    first_name, last_name, is_staff, is_active,
    is_superuser, date_joined, email
) VALUES (
    ?, ?, 1, 'buyer',
    'Guest', 'User', 0, 1,
    0, CURRENT_TIMESTAMP, ''
);
```

**Parameters**: auto_generated_username (e.g., 'guest_a7f3b9c2d4e1'), random_password

### Query 10.2: Delete Guest on Logout

```sql
DELETE FROM users_customuser
WHERE id = ? AND is_guest = 1;
```

**Parameters**: guest_user_id

### Query 10.3: Cleanup Old Guests (Maintenance)

```sql
DELETE FROM users_customuser
WHERE is_guest = 1
  AND last_login < datetime('now', '-1 day');
```

---

## 📈 ADDITIONAL ANALYTICS QUERIES

### A1: Most Popular Cars

```sql
SELECT
    c.*, u.username as seller_name,
    COUNT(DISTINCT cv.customuser_id) as unique_viewers
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
LEFT JOIN cars_car_viewed_by cv ON c.id = cv.car_id
WHERE c.is_sold = 0
GROUP BY c.id
ORDER BY c.views DESC, unique_viewers DESC
LIMIT 10;
```

### A2: Recently Sold Cars

```sql
SELECT c.*, u.username as seller_name
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE c.is_sold = 1
ORDER BY c.date_posted DESC
LIMIT 10;
```

### A3: Price Statistics by Make

```sql
SELECT
    make,
    COUNT(*) as car_count,
    AVG(price) as avg_price,
    MIN(price) as min_price,
    MAX(price) as max_price
FROM cars_car
WHERE is_sold = 0
GROUP BY make
HAVING COUNT(*) >= 3
ORDER BY avg_price DESC;
```

### A4: Seller Activity Report

```sql
SELECT
    u.id, u.username, u.role,
    COUNT(c.id) as listings_posted,
    SUM(c.views) as total_views,
    SUM(CASE WHEN c.is_sold = 1 THEN 1 ELSE 0 END) as cars_sold,
    AVG(c.price) as avg_price
FROM users_customuser u
LEFT JOIN cars_car c ON u.id = c.seller_id
WHERE u.role = 'seller' AND u.is_guest = 0
GROUP BY u.id
ORDER BY listings_posted DESC;
```

### A5: Price Range Distribution

```sql
SELECT
    CASE
        WHEN price < 10000 THEN 'Under $10k'
        WHEN price BETWEEN 10000 AND 20000 THEN '$10k-$20k'
        WHEN price BETWEEN 20000 AND 30000 THEN '$20k-$30k'
        WHEN price BETWEEN 30000 AND 50000 THEN '$30k-$50k'
        ELSE 'Over $50k'
    END as price_range,
    COUNT(*) as count,
    AVG(price) as avg_in_range
FROM cars_car
WHERE is_sold = 0
GROUP BY price_range
ORDER BY MIN(price);
```

### A6: Most Active Buyers (by views)

```sql
SELECT
    u.id, u.username, u.role,
    COUNT(DISTINCT cv.car_id) as cars_viewed
FROM users_customuser u
INNER JOIN cars_car_viewed_by cv ON u.id = cv.customuser_id
WHERE u.role = 'buyer' AND u.is_guest = 0
GROUP BY u.id
ORDER BY cars_viewed DESC
LIMIT 20;
```

### A7: Role Distribution

```sql
SELECT
    role,
    is_guest,
    COUNT(*) as user_count
FROM users_customuser
GROUP BY role, is_guest
ORDER BY user_count DESC;
```

### A8: View Engagement Rate

```sql
SELECT
    c.id, c.make, c.model,
    c.views as total_views,
    COUNT(DISTINCT cv.customuser_id) as unique_viewers,
    CAST(COUNT(DISTINCT cv.customuser_id) AS FLOAT) / NULLIF(c.views, 0) as engagement_rate
FROM cars_car c
LEFT JOIN cars_car_viewed_by cv ON c.id = cv.car_id
WHERE c.is_sold = 0
GROUP BY c.id
ORDER BY unique_viewers DESC
LIMIT 20;
```

---

## 🎯 DJANGO ORM EQUIVALENTS

For developers, here are the Django ORM equivalents:

```python
# SCREEN 1: Home
Car.objects.filter(is_sold=False).order_by('-date_posted')[:8]
Car.objects.filter(is_sold=False).count()

# SCREEN 2: Register
CustomUser.objects.create_user(username=?, password=?, role=?, ...)

# SCREEN 3: Login
CustomUser.objects.get(username=?, is_active=True)

# SCREEN 4: Browse
Car.objects.filter(is_sold=False).select_related('seller')
Car.objects.filter(Q(make__icontains=q) | Q(model__icontains=q))

# SCREEN 5: Detail
Car.objects.select_related('seller').get(pk=id)
car.viewed_by.add(user)  # Track view
car.viewed_by.filter(id=user_id).exists()  # Check

# SCREEN 6: Profile
user.cars.all()
user.cars.aggregate(Count('id'), Sum('views'))

# SCREEN 7: Post Car
Car.objects.create(seller=user, ...)

# SCREEN 8: Edit
Car.objects.filter(pk=id, seller=user).update(...)

# SCREEN 9: Delete
Car.objects.filter(pk=id, seller=user).delete()

# SCREEN 10: Guest
CustomUser.objects.create_user(username='guest_...', is_guest=True)
CustomUser.objects.filter(id=id, is_guest=True).delete()
```

---

## ⚡ PERFORMANCE OPTIMIZATION

### Indexed Columns:

- `users_customuser`: username, email, role, is_guest
- `cars_car`: seller_id, make, price, is_sold, date_posted, transmission, fuel_type
- `cars_car_viewed_by`: car_id, customuser_id

### Best Practices:

1. Always filter by `is_sold = 0` for available cars
2. Use `INNER JOIN` for required relationships
3. Apply `LIMIT` for pagination
4. Use `UNIQUE` constraint on viewed_by for data integrity
5. Leverage indexes for WHERE and ORDER BY clauses
6. Use `COALESCE` for conditional updates
7. Use `CASCADE` for automatic cleanup

---

**Total Screens**: 10  
**Total Core Queries**: 60+  
**Database Tables**: 3  
**Indexes**: 13

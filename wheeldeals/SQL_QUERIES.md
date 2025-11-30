# SQL Queries Documentation - WheelDeals Project

This document contains all SQL queries used in the WheelDeals application, organized by screen/functionality.

## Database Schema

### Table: users_customuser

```sql
CREATE TABLE users_customuser (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME,
    is_superuser BOOL NOT NULL,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOL NOT NULL,
    is_active BOOL NOT NULL,
    date_joined DATETIME NOT NULL,
    phone VARCHAR(15),
    city VARCHAR(100)
);

CREATE INDEX idx_users_username ON users_customuser(username);
CREATE INDEX idx_users_email ON users_customuser(email);
```

### Table: cars_car

```sql
CREATE TABLE cars_car (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    mileage INTEGER,
    color VARCHAR(50),
    transmission VARCHAR(20),
    fuel_type VARCHAR(20),
    description TEXT,
    image1 VARCHAR(100),
    image2 VARCHAR(100),
    image3 VARCHAR(100),
    seller_id INTEGER NOT NULL,
    date_posted DATETIME NOT NULL,
    is_sold BOOL NOT NULL DEFAULT 0,
    views INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (seller_id) REFERENCES users_customuser(id) ON DELETE CASCADE
);

CREATE INDEX idx_cars_seller ON cars_car(seller_id);
CREATE INDEX idx_cars_make ON cars_car(make);
CREATE INDEX idx_cars_price ON cars_car(price);
CREATE INDEX idx_cars_is_sold ON cars_car(is_sold);
CREATE INDEX idx_cars_date_posted ON cars_car(date_posted DESC);
```

---

## Screen 1: Home Page

### Query 1: Get Recent Cars

```sql
SELECT * FROM cars_car
WHERE is_sold = 0
ORDER BY date_posted DESC
LIMIT 8;
```

### Query 2: Count Total Available Cars

```sql
SELECT COUNT(*) as total_cars
FROM cars_car
WHERE is_sold = 0;
```

---

## Screen 2: User Registration

### Query: Insert New User

```sql
INSERT INTO users_customuser (
    username,
    email,
    password,
    first_name,
    last_name,
    phone,
    city,
    is_staff,
    is_active,
    is_superuser,
    date_joined
) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 1, 0, CURRENT_TIMESTAMP);
```

### Query: Check Username Availability

```sql
SELECT COUNT(*)
FROM users_customuser
WHERE username = ?;
```

---

## Screen 3: User Login

### Query 1: Authenticate User

```sql
SELECT id, username, password, email, first_name, last_name, phone, city
FROM users_customuser
WHERE username = ? AND is_active = 1;
```

### Query 2: Update Last Login

```sql
UPDATE users_customuser
SET last_login = CURRENT_TIMESTAMP
WHERE id = ?;
```

---

## Screen 4: Car Listings / Browse Cars

### Query 1: Get All Available Cars (with pagination)

```sql
SELECT
    c.id,
    c.make,
    c.model,
    c.year,
    c.price,
    c.mileage,
    c.color,
    c.transmission,
    c.fuel_type,
    c.image1,
    c.views,
    c.date_posted,
    u.username as seller_name,
    u.phone as seller_phone
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE c.is_sold = 0
ORDER BY c.date_posted DESC
LIMIT 12 OFFSET ?;
```

### Query 2: Count Total Cars (for pagination)

```sql
SELECT COUNT(*)
FROM cars_car
WHERE is_sold = 0;
```

### Query 3: Search Cars by Make/Model

```sql
SELECT c.*, u.username as seller_name
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE (c.make LIKE '%?%' OR c.model LIKE '%?%' OR c.description LIKE '%?%')
  AND c.is_sold = 0
ORDER BY c.date_posted DESC;
```

### Query 4: Filter Cars by Price Range

```sql
SELECT c.*, u.username as seller_name
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE c.price BETWEEN ? AND ?
  AND c.is_sold = 0
ORDER BY c.price ASC;
```

### Query 5: Filter by Transmission Type

```sql
SELECT c.*, u.username as seller_name
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE c.transmission = ?
  AND c.is_sold = 0
ORDER BY c.date_posted DESC;
```

### Query 6: Filter by Fuel Type

```sql
SELECT c.*, u.username as seller_name
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE c.fuel_type = ?
  AND c.is_sold = 0
ORDER BY c.date_posted DESC;
```

### Query 7: Combined Filters

```sql
SELECT c.*, u.username as seller_name
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE c.make LIKE '%?%'
  AND c.price BETWEEN ? AND ?
  AND c.transmission = ?
  AND c.fuel_type = ?
  AND c.is_sold = 0
ORDER BY c.date_posted DESC
LIMIT 12 OFFSET ?;
```

---

## Screen 5: Car Detail Page

### Query 1: Get Car Details with Seller Info

```sql
SELECT
    c.*,
    u.username,
    u.first_name,
    u.last_name,
    u.email,
    u.phone,
    u.city
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE c.id = ?;
```

### Query 2: Increment View Count

```sql
UPDATE cars_car
SET views = views + 1
WHERE id = ?;
```

### Query 3: Get Related Cars (Same Make)

```sql
SELECT *
FROM cars_car
WHERE make = ?
  AND id != ?
  AND is_sold = 0
ORDER BY date_posted DESC
LIMIT 4;
```

---

## Screen 6: Add/Post Car

### Query: Insert New Car Listing

```sql
INSERT INTO cars_car (
    make,
    model,
    year,
    price,
    mileage,
    color,
    transmission,
    fuel_type,
    description,
    image1,
    image2,
    image3,
    seller_id,
    date_posted,
    is_sold,
    views
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, 0, 0);
```

---

## Screen 7: Edit User Profile

### Query 1: Get User Profile Data

```sql
SELECT *
FROM users_customuser
WHERE id = ?;
```

### Query 2: Update User Profile

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

### Query 3: Get User's Car Listings

```sql
SELECT *
FROM cars_car
WHERE seller_id = ?
ORDER BY date_posted DESC;
```

---

## Additional Queries

### Update Car Listing

```sql
UPDATE cars_car
SET
    make = ?,
    model = ?,
    year = ?,
    price = ?,
    mileage = ?,
    color = ?,
    transmission = ?,
    fuel_type = ?,
    description = ?
WHERE id = ? AND seller_id = ?;
```

### Delete Car Listing

```sql
DELETE FROM cars_car
WHERE id = ? AND seller_id = ?;
```

### Mark Car as Sold

```sql
UPDATE cars_car
SET is_sold = 1
WHERE id = ?;
```

### Get User Statistics

```sql
SELECT
    COUNT(*) as total_listings,
    SUM(CASE WHEN is_sold = 1 THEN 1 ELSE 0 END) as sold_count,
    SUM(views) as total_views
FROM cars_car
WHERE seller_id = ?;
```

### Get Popular Cars (Most Viewed)

```sql
SELECT c.*, u.username as seller_name
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE c.is_sold = 0
ORDER BY c.views DESC
LIMIT 10;
```

### Get Recently Sold Cars

```sql
SELECT c.*, u.username as seller_name
FROM cars_car c
INNER JOIN users_customuser u ON c.seller_id = u.id
WHERE c.is_sold = 1
ORDER BY c.date_posted DESC
LIMIT 10;
```

### Average Price by Make

```sql
SELECT
    make,
    AVG(price) as avg_price,
    COUNT(*) as count
FROM cars_car
WHERE is_sold = 0
GROUP BY make
ORDER BY avg_price DESC;
```

### Cars by Year Range

```sql
SELECT *
FROM cars_car
WHERE year BETWEEN ? AND ?
  AND is_sold = 0
ORDER BY year DESC;
```

---

## Performance Optimization Notes

1. **Indexes**: Created on frequently queried columns (username, email, seller_id, make, price, is_sold, date_posted)
2. **JOIN Optimization**: Used INNER JOIN for seller information to avoid NULL checks
3. **Pagination**: Used LIMIT and OFFSET for efficient pagination
4. **Selective Loading**: Only load required columns when possible
5. **Caching**: Consider caching frequently accessed data (home page, popular cars)

---

## Django ORM Equivalents

For reference, here are Django ORM queries that generate the above SQL:

```python
# Get all available cars
Car.objects.filter(is_sold=False).select_related('seller').order_by('-date_posted')

# Search cars
Car.objects.filter(Q(make__icontains=query) | Q(model__icontains=query))

# Get car with seller
Car.objects.select_related('seller').get(pk=id)

# Create new car
Car.objects.create(make='Toyota', model='Camry', ...)

# Update car
car.update(price=25000)

# Delete car
car.delete()

# Count cars
Car.objects.filter(is_sold=False).count()

# Get user's cars
request.user.cars.all()
```

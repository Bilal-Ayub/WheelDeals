# Guest User Feature Implementation

## Overview

This document describes the guest user functionality added to the WheelDeals Django project. Guest users allow anonymous browsing with unique view counting and contact information masking.

## Database Changes

### 1. CustomUser Model (`users/models.py`)

**New Field:**

- `is_guest` (BooleanField): Marks whether a user is a guest (default: False)

**SQL:**

```sql
ALTER TABLE users_customuser ADD COLUMN is_guest BOOL NOT NULL DEFAULT 0;
```

### 2. Car Model (`cars/models.py`)

**New Field:**

- `viewed_by` (ManyToManyField): Tracks which users have viewed each car listing

**SQL:**

```sql
CREATE TABLE cars_car_viewed_by (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER NOT NULL,
    customuser_id INTEGER NOT NULL,
    FOREIGN KEY (car_id) REFERENCES cars_car(id),
    FOREIGN KEY (customuser_id) REFERENCES users_customuser(id),
    UNIQUE(car_id, customuser_id)
);
```

## Key Features

### 1. Guest User Creation

**Location:** `users/utils.py`

**Function:** `create_guest_user(request)`

- Automatically creates a guest user with unique username (guest_XXXXXXXXXXXX)
- Sets random password
- Marks user as guest with `is_guest=True`
- Automatically logs in the guest user

### 2. Unique View Counting

**Location:** `cars/views.py` - `car_detail()` function

**How it works:**

- Each user (including guests) is tracked via the `viewed_by` ManyToMany relationship
- View count only increments if the user hasn't viewed the car before
- Provides accurate unique visitor statistics

**SQL Queries:**

```sql
-- Check if user has viewed the car
SELECT COUNT(*) FROM cars_car_viewed_by
WHERE car_id = ? AND customuser_id = ?;

-- Add user to viewed_by if not already present
INSERT INTO cars_car_viewed_by (car_id, customuser_id)
VALUES (?, ?);

-- Increment view count
UPDATE cars_car SET views = views + 1 WHERE id = ?;
```

### 3. Contact Information Masking

**Location:** `templates/cars/car_detail.html`

**For Guest Users:**

- Email: Shows "Email hidden - Sign up to view"
- Phone: Shows "+XX XXXXXXXXXX"
- Warning message prompting sign up/login

**For Registered Users:**

- Full contact information visible
- Can send email to seller

### 4. Homepage Guest Buttons

**Location:** `templates/home.html`

**When NOT logged in:**

- "Browse Cars as Guest" button (primary action)
- "Login" button
- "Sign Up" button
- "Continue as Guest" button (alternative option)

**When logged in as Guest:**

- "Browse Cars" button
- "Sign Up to Sell" button (guests can't create listings)

**When logged in as Registered User:**

- "Browse Cars" button
- "Sell Your Car" button

### 5. Navigation Bar Updates

**Location:** `templates/base.html`

**Guest Mode Shows:**

- "Guest Mode" indicator (yellow badge)
- "Sign Up" link
- "End Session" button (deletes guest account on logout)

### 6. Guest Restrictions

Guests cannot:

- Create car listings (`car_create` redirects to register)
- Access profile page (`profile` redirects to register)
- View seller contact information
- Send emails to sellers

### 7. Guest Session Management

**Location:** `users/views.py` - `user_logout()` function

**Behavior:**

- When a guest logs out, their account is automatically **deleted**
- This prevents database clutter from temporary guest accounts
- Regular users are logged out normally without deletion

## URL Routes

### New Route:

- `/users/guest/` - Creates guest user and redirects to home (name: `continue_as_guest`)

## User Flow Examples

### Guest User Journey:

1. Visit homepage (not logged in)
2. Click "Continue as Guest" or "Browse Cars as Guest"
3. System auto-creates guest account (e.g., guest_a7f3b9c2d4e1)
4. Guest logs in automatically
5. Can browse cars and see masked contact info
6. Viewing a car increments unique view count
7. Viewing same car again does NOT increment count
8. Guest clicks "End Session" → account deleted

### Upgrading Guest to Registered User:

1. Guest browses as guest
2. Clicks "Sign Up" in navbar or contact warning
3. Registers with real credentials
4. Previous guest account remains (separate from new account)
5. View history doesn't transfer (limitation)

## Testing Scenarios

### Test 1: Unique View Counting

1. Create guest user A → view car #1 (views = 1)
2. Guest A views car #1 again (views = still 1)
3. Create guest user B → view car #1 (views = 2)
4. Registered user views car #1 (views = 3)

### Test 2: Contact Masking

1. As guest, view car detail
2. Verify phone shows "+XX XXXXXXXXXX"
3. Verify email shows "Email hidden - Sign up to view"
4. Sign up and login
5. View same car → full contact info visible

### Test 3: Guest Restrictions

1. As guest, try to access `/users/profile/` → redirected to register
2. As guest, try to access `/cars/create/` → redirected to register
3. As guest, click "Contact Seller" button → should be disabled

## SQL Queries Documentation

### Get all guest users:

```sql
SELECT * FROM users_customuser WHERE is_guest = 1;
```

### Get unique viewers for a car:

```sql
SELECT u.username, u.is_guest
FROM users_customuser u
JOIN cars_car_viewed_by cv ON u.id = cv.customuser_id
WHERE cv.car_id = ?;
```

### Delete all guest users (cleanup):

```sql
DELETE FROM users_customuser WHERE is_guest = 1;
```

### Get view statistics by car:

```sql
SELECT
    c.id,
    c.make,
    c.model,
    c.views,
    COUNT(cv.customuser_id) as unique_viewers
FROM cars_car c
LEFT JOIN cars_car_viewed_by cv ON c.id = cv.car_id
GROUP BY c.id;
```

## Future Enhancements

Potential improvements:

1. **Session-based guests**: Use sessions instead of database records for guests
2. **View duration tracking**: Track how long users view each listing
3. **Guest conversion tracking**: Track which guests sign up
4. **Guest wishlist**: Allow guests to save cars to session (lost on logout)
5. **Rate limiting**: Prevent guest account abuse
6. **Analytics dashboard**: Show guest vs registered user metrics

## Files Modified

1. `users/models.py` - Added is_guest field
2. `cars/models.py` - Added viewed_by ManyToMany field
3. `users/utils.py` - Created (new file) with guest utilities
4. `users/views.py` - Added guest creation and restrictions
5. `users/urls.py` - Added guest route
6. `cars/views.py` - Updated view counting and guest auto-creation
7. `templates/home.html` - Added guest buttons
8. `templates/base.html` - Added guest mode indicator in navbar
9. `templates/cars/car_detail.html` - Added contact masking for guests
10. Migrations:
    - `users/migrations/0002_customuser_is_guest.py`
    - `cars/migrations/0003_car_viewed_by.py`

## Benefits

1. **Better Analytics**: Unique view counting provides accurate engagement metrics
2. **Lower Barrier to Entry**: Users can browse without creating account
3. **Privacy**: Contact information protected from casual browsers
4. **Conversion Funnel**: Guests see value before committing to signup
5. **Clean Database**: Auto-deletion prevents guest account accumulation

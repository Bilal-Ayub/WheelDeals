# User Roles Feature Implementation

## Overview

This document describes the user role-based access control system added to WheelDeals. Users can register as either **Buyer** or **Seller**, with different capabilities for each role.

## Database Changes

### CustomUser Model (`users/models.py`)

**New Field:**

- `role` (CharField): Stores user role - either 'buyer' or 'seller' (default: 'buyer')

**SQL:**

```sql
ALTER TABLE users_customuser ADD COLUMN role VARCHAR(10) NOT NULL DEFAULT 'buyer';
```

**New Methods:**

- `is_buyer()`: Returns True if user is a buyer
- `is_seller()`: Returns True if user is a seller

## User Roles

### BUYER Role

**Capabilities:**

- ✅ Search and filter car listings
- ✅ View car details and photos
- ✅ View full seller contact information (when logged in)
- ✅ Manage personal profile
- ✅ Browse all listings

**Restrictions:**

- ❌ Cannot post car listings
- ❌ Cannot manage car ads
- ❌ "Sell Car" link not shown in navigation

**Access Control:**

- Can browse without restrictions
- Contact information visible for all listings
- Profile shows "Buyer" badge

### SELLER Role

**Capabilities:**

- ✅ Post new car listings
- ✅ Edit existing listings (own cars only)
- ✅ Delete listings (own cars only)
- ✅ View listing metrics (views, status)
- ✅ Manage profile
- ✅ Browse other sellers' listings

**Access Control:**

- "Sell Car" option in navigation menu
- Car management section in profile
- Profile shows "Seller" badge

## Registration Process

### Sign-Up Form Updates

**Location:** `templates/users/register.html`

**New Field: Role Selection**

- Visual card-based selection
- Two options: Buyer or Seller
- Icons and descriptions for each role
- Radio button input (required field)
- Default selection: Buyer

**Form Fields:**

1. Username \*
2. First Name \*
3. Last Name \*
4. Email \*
5. Phone
6. City
7. **Role Selection\*** (NEW)
   - Buyer: "Search and view car listings"
   - Seller: "Post and manage car ads"
8. Password \*
9. Confirm Password \*

## UI Changes

### 1. Navigation Bar (`templates/base.html`)

**For Sellers:**

```
Home | Browse Cars | Sell Car | Profile | Logout
```

**For Buyers:**

```
Home | Browse Cars | Profile | Logout
```

**For Guests:**

```
Home | Browse Cars | Guest Mode | Sign Up | End Session
```

### 2. Homepage (`templates/home.html`)

**Logged in as Seller:**

- "Browse Cars" button
- "Sell Your Car" button

**Logged in as Buyer:**

- "Browse Cars" button
- "My Profile" button

**Not logged in:**

- "Sign Up" and "Log In" buttons (side by side)
- "Continue as guest" button (below)

### 3. Profile Page (`templates/users/profile.html`)

**For Sellers:**

- Profile information with "Seller" badge
- "My Car Listings" section
  - Table showing all listings
  - Metrics: views, price, status
  - Actions: View, Edit, Delete
  - "Add New" button

**For Buyers:**

- Profile information with "Buyer" badge
- "My Activity" section
  - Message: "You're registered as a Buyer"
  - "Browse Cars" button

## Access Restrictions

### 1. Car Creation (`cars/views.py` - `car_create()`)

```python
# Check 1: Not a guest
if is_guest_user(request.user):
    redirect to register

# Check 2: Must be a seller
if not request.user.is_seller():
    show warning message
    redirect to home
```

**Error Messages:**

- Guest: "Please sign up to list your car for sale."
- Buyer: "Only Sellers can post car listings. Your account is registered as a Buyer."

### 2. Navigation Links

- "Sell Car" link only visible to sellers
- Buyers see profile link instead

### 3. Profile Sections

- Car listings section only for sellers
- Buyers see activity/browse section

## SQL Queries

### Check user role:

```sql
SELECT role FROM users_customuser WHERE id = ?;
```

### Get all sellers:

```sql
SELECT * FROM users_customuser WHERE role = 'seller';
```

### Get all buyers:

```sql
SELECT * FROM users_customuser WHERE role = 'buyer';
```

### Get seller's cars:

```sql
SELECT c.*, u.username, u.role
FROM cars_car c
JOIN users_customuser u ON c.seller_id = u.id
WHERE u.id = ? AND u.role = 'seller';
```

### Count users by role:

```sql
SELECT role, COUNT(*) as count
FROM users_customuser
WHERE is_guest = 0
GROUP BY role;
```

## Permission Matrix

| Feature             | Guest | Buyer | Seller | Notes                     |
| ------------------- | ----- | ----- | ------ | ------------------------- |
| View Homepage       | ✅    | ✅    | ✅     | Public                    |
| Browse Cars         | ✅    | ✅    | ✅     | Public                    |
| View Car Details    | ✅    | ✅    | ✅     | Contact masked for guests |
| View Contact Info   | ❌    | ✅    | ✅     | Hidden for guests         |
| Post Car Listing    | ❌    | ❌    | ✅     | Sellers only              |
| Edit Car Listing    | ❌    | ❌    | ✅     | Own cars only             |
| Delete Car Listing  | ❌    | ❌    | ✅     | Own cars only             |
| View Profile        | ❌    | ✅    | ✅     | Registered users          |
| Manage Car Listings | ❌    | ❌    | ✅     | Sellers only              |

## User Journey Examples

### Buyer Registration:

1. Click "Sign Up" on homepage
2. Fill in personal details
3. Select **"Buyer"** role
4. Submit form
5. Login
6. Can browse cars and view contact info
7. No "Sell Car" option visible

### Seller Registration:

1. Click "Sign Up" on homepage
2. Fill in personal details
3. Select **"Seller"** role
4. Submit form
5. Login
6. "Sell Car" appears in navigation
7. Can post and manage listings

### Buyer Trying to Sell:

1. Buyer logs in
2. Navigates to `/cars/add/` directly
3. System checks role
4. Redirects to home with warning message
5. "Only Sellers can post car listings..."

## Testing Scenarios

### Test 1: Role Selection During Registration

1. Go to sign-up page
2. Verify role selection shows Buyer and Seller options
3. Select Buyer → Submit → Check database (role='buyer')
4. Register another user as Seller → Check database (role='seller')

### Test 2: Seller Permissions

1. Login as Seller
2. Verify "Sell Car" in navigation
3. Go to profile → See car listings section
4. Post a car → Success
5. View posted car → Can edit/delete

### Test 3: Buyer Restrictions

1. Login as Buyer
2. Verify NO "Sell Car" in navigation
3. Try to access `/cars/add/` directly → Redirected with error
4. Go to profile → See "My Activity" instead of listings
5. Browse cars → Can view all details and contact info

### Test 4: Guest vs Buyer Contact Visibility

1. As guest → View car → Contact masked
2. Sign up as Buyer → Login
3. View same car → Contact info visible

## Future Enhancements

Potential improvements:

1. **Role Upgrade**: Allow buyers to upgrade to seller (add UI)
2. **Dual Role**: Support users being both buyer and seller
3. **Role-specific Dashboard**: Different analytics for each role
4. **Seller Verification**: Badge for verified sellers
5. **Buyer Wishlist**: Save favorite listings
6. **Inspection Requests**: Buyers request car inspections (planned)
7. **Messaging System**: Direct buyer-seller communication
8. **Transaction History**: Track purchases/sales

## Files Modified

1. `users/models.py` - Added role field and helper methods
2. `users/forms.py` - Added role selection to registration form
3. `users/views.py` - No changes needed (role automatically saved)
4. `cars/views.py` - Added seller-only restriction to car_create
5. `templates/users/register.html` - Added visual role selection
6. `templates/base.html` - Conditional navigation based on role
7. `templates/home.html` - Role-based button display
8. `templates/users/profile.html` - Different sections for buyers/sellers
9. Migration: `users/migrations/0003_customuser_role.py`

## Benefits

1. **Clear User Segregation**: Buyers and sellers have distinct experiences
2. **Simplified UI**: Users only see relevant features
3. **Data Integrity**: Prevents buyers from accidentally creating listings
4. **Better Analytics**: Can track metrics separately for each role
5. **Scalability**: Easy to add role-specific features in future
6. **Security**: Role-based access control at view level

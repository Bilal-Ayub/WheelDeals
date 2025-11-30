# WheelDeals - Quick Reference Guide

## User Roles & Permissions

### Guest Users

- **Access**: Browse listings, view masked contact info
- **Restrictions**: Cannot see full contact details, cannot post ads
- **Auto-created**: When clicking "Continue as guest" or browsing cars
- **Deleted**: Account automatically deleted on logout

### Buyer Role

- **Registration**: Select "Buyer" during sign-up
- **Can Do**:
  - Search and filter car listings
  - View full seller contact information
  - Manage personal profile
  - Browse all listings
- **Cannot Do**:
  - Post car listings
  - Edit/delete car ads
  - Access seller features
- **Badge**: Blue "Buyer" badge in profile

### Seller Role

- **Registration**: Select "Seller" during sign-up
- **Can Do**:
  - Post new car listings
  - Edit own listings
  - Delete own listings
  - View listing metrics (views, status)
  - Manage profile
  - Browse other listings
- **Navigation**: "Sell Car" option visible
- **Badge**: Green "Seller" badge in profile

## How to Use Each Feature

### As a Guest:

1. Visit homepage
2. Click "Continue as guest" or "Browse Cars as Guest"
3. View cars with masked contact (+XX XXXXXXXXXX)
4. Sign up to see full details

### As a Buyer:

1. Sign up and select "Buyer" role
2. Login
3. Browse cars → see full contact information
4. Use search/filters to find cars
5. Contact sellers directly via email/phone

### As a Seller:

1. Sign up and select "Seller" role
2. Login
3. Click "Sell Car" in navigation
4. Fill in car details and upload photos
5. Manage listings from profile page
6. Edit/delete listings as needed

## Key Features

### Unique View Counting

- Each user (including guests) counted once per listing
- Viewing same car multiple times = 1 view
- Provides accurate analytics

### Contact Information

- **Guests**: Phone masked, email hidden
- **Buyers**: Full contact visible
- **Sellers**: Full contact visible

### Profile Management

- **Buyers**: See activity dashboard
- **Sellers**: See car listings table with metrics

## Admin Access

- Login at: `/admin/`
- View all users with roles
- Filter by: Buyer, Seller, Guest
- Manage user accounts and listings

## Database Structure

### Users Table:

- username, email, password
- first_name, last_name
- phone, city
- **role** (buyer/seller)
- **is_guest** (true/false)

### Cars Table:

- make, model, year, price
- mileage, color, transmission, fuel_type
- description, images (3 photos max)
- seller_id (foreign key to users)
- is_sold, views
- **viewed_by** (many-to-many with users)

## URL Routes

### Public:

- `/` - Homepage
- `/cars/` - Browse cars
- `/cars/<id>/` - Car detail
- `/users/register/` - Sign up
- `/users/login/` - Login
- `/users/guest/` - Create guest account

### Authenticated:

- `/users/profile/` - User profile
- `/users/logout/` - Logout

### Sellers Only:

- `/cars/add/` - Post new car
- `/cars/<id>/edit/` - Edit car
- `/cars/<id>/delete/` - Delete car

## Testing Accounts

### Create Test Accounts:

```python
# Buyer account
python manage.py shell
from users.models import CustomUser
buyer = CustomUser.objects.create_user(
    username='testbuyer',
    password='testpass123',
    email='buyer@test.com',
    role='buyer'
)

# Seller account
seller = CustomUser.objects.create_user(
    username='testseller',
    password='testpass123',
    email='seller@test.com',
    role='seller'
)
```

## Common Issues

### "Only Sellers can post car listings"

- Your account is registered as Buyer
- You need a Seller account to post ads
- Create new account with Seller role

### Contact information hidden

- You're browsing as Guest
- Sign up or login to see full contact details

### "Sell Car" not showing in menu

- Your account is Buyer role
- Only Sellers see this option
- Buyers can browse and view contacts

## Next Steps (Future Features)

1. **Inspection Requests**: Buyers request car inspections
2. **Messaging System**: Direct buyer-seller chat
3. **Wishlist**: Save favorite cars
4. **Advanced Search**: More filters and sorting
5. **Analytics Dashboard**: Detailed seller metrics
6. **Role Upgrade**: Convert Buyer to Seller account

## Support

For issues or questions:

- Check error messages carefully
- Verify your account role in Profile page
- Ensure you're logged in for full features
- Guest mode has limited access by design

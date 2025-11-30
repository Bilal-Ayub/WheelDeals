# Admin Role Implementation Guide

## Overview

The admin role has been successfully implemented in WheelDeals with comprehensive system management capabilities.

---

## Admin Role Features

### 1. **Ad Moderation**

- **Pending Ads**: Review all car listings awaiting approval
- **Approve/Decline**: Approve listings to make them public or decline with reason
- **Status Management**: Track ads as pending, published, or declined
- **Seller Notifications**: Declined ads show reason to sellers

### 2. **User Management**

- **View All Users**: Complete list with filtering by role
- **Edit User Roles**: Change any user's role (buyer, seller, inspector, admin)
- **Delete Users**: Remove user accounts (cannot delete own account)
- **User Statistics**: Track user activity and login history

### 3. **Inspection Oversight**

- **View All Inspections**: Complete visibility into all inspection requests
- **Status Filtering**: Filter by requested, accepted, assigned, in_progress, completed, rejected
- **Reassign Inspectors**: Change assigned inspector for any inspection
- **Dispute Resolution**: Monitor and intervene in inspection workflows
- **View Reports**: Access all completed inspection reports

### 4. **Analytics Dashboard**

- **User Statistics**:
  - Total users count
  - Breakdown: Buyers, Sellers, Inspectors
  - Currently online users
- **Ad Statistics**:
  - Total ads posted
  - Pending approval requests
  - Published ads
  - Declined ads
- **Inspection Statistics**:
  - Total inspections
  - Completed inspections
  - In-progress inspections
- **Charts & Visualizations**:
  - Pie chart: Ads by city
  - Bar chart: Ads by car make

### 5. **Listing Management**

- **View All Listings**: Complete car inventory with status
- **Delete Any Listing**: Remove any car ad permanently
- **Status Filtering**: Filter by pending, published, declined

---

## Creating an Admin User

### Method 1: Django Shell (Recommended)

```bash
# Activate virtual environment
.\my_env\Scripts\Activate.ps1

# Open Django shell
python manage.py shell

# Create admin user
from users.models import CustomUser
admin = CustomUser.objects.create_user(
    username='admin',
    password='admin123',  # Change this!
    email='admin@wheeldeals.com',
    first_name='Admin',
    last_name='User',
    role='admin'
)
admin.is_staff = True  # Optional: Django admin access
admin.is_superuser = True  # Optional: Full Django admin rights
admin.save()
print(f"Admin user created: {admin.username}")
```

### Method 2: Django Admin Panel

1. Create a superuser first:
   ```bash
   python manage.py createsuperuser
   ```
2. Login to Django admin: `http://127.0.0.1:8000/admin/`
3. Go to Users
4. Create new user or edit existing user
5. Set role to "Admin"

### Method 3: Direct Database Update (For Testing Only)

```bash
# Update existing user to admin
python -c "import django; import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wheeldeals_project.settings'); django.setup(); from users.models import CustomUser; user = CustomUser.objects.get(username='YOUR_USERNAME'); user.role='admin'; user.save(); print(f'{user.username} is now admin')"
```

---

## Admin Panel Access

### URL

`http://127.0.0.1:8000/admin-panel/`

### Navigation

- Visible in navbar when logged in as admin (yellow "Admin Panel" link)
- Only accessible to users with `role='admin'`
- Protected by `@admin_required` decorator

### Admin Panel URLs

- **Dashboard**: `/admin-panel/`
- **Pending Ads**: `/admin-panel/pending-ads/`
- **User Management**: `/admin-panel/users/`
- **Inspection Oversight**: `/admin-panel/inspections/`
- **All Listings**: `/admin-panel/all-listings/`

---

## Security Features

### 1. **Role Restriction**

- Admin role **cannot** be selected during normal signup
- Only visible in Django admin or via shell
- Prevents self-promotion to admin

### 2. **Access Protection**

- All admin views protected by `@admin_required` decorator
- Redirects unauthorized users to home page
- Shows error message for non-admin access attempts

### 3. **Self-Protection**

- Admin cannot delete their own account
- Prevents accidental lockout

---

## Ad Moderation Workflow

### New Listings Flow

1. **Seller Posts Car** → Status: `pending`
2. **Admin Reviews** → Admin Panel → Pending Ads
3. **Admin Decision**:
   - **Approve** → Status: `published` (visible to all users)
   - **Decline** → Status: `declined` + reason saved
4. **Seller Notification** → Message shown on listing

### Published Cars

- Visible on home page
- Visible in browse/search results
- Public inspection reports shown

### Declined Cars

- **Not visible** to public
- Seller can still view their own listing
- Decline reason displayed to seller
- Seller can edit and resubmit (stays pending)

---

## Database Schema Updates

### Users Model Changes

```python
ROLE_CHOICES = [
    ("buyer", "Buyer"),
    ("seller", "Seller"),
    ("inspector", "Inspector"),
    ("admin", "Admin"),  # NEW
]

def is_admin(self):
    return self.role == "admin"
```

### Cars Model Changes

```python
STATUS_CHOICES = [
    ("pending", "Pending Review"),      # NEW
    ("published", "Published"),         # NEW
    ("declined", "Declined"),           # NEW
]

status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default="pending"
)

declined_reason = models.TextField(blank=True)
```

### Migrations Applied

- `users/migrations/0005_alter_customuser_role.py` - Added admin role
- `cars/migrations/0004_car_declined_reason_car_status.py` - Added status & reason fields
- All existing cars set to `published` status

---

## Testing the Admin Role

### Quick Test Steps

1. **Create Admin User**:

   ```bash
   python manage.py shell
   >>> from users.models import CustomUser
   >>> admin = CustomUser.objects.create_user(
   ...     username='testadmin',
   ...     password='test123',
   ...     role='admin',
   ...     email='admin@test.com'
   ... )
   >>> exit()
   ```

2. **Login as Admin**:

   - Go to `http://127.0.0.1:8000/users/login/`
   - Username: `testadmin`, Password: `test123`
   - Yellow "Admin Panel" link appears in navbar

3. **Test Dashboard**:

   - Click "Admin Panel"
   - View statistics cards
   - Check charts display correctly

4. **Test Ad Moderation**:

   - Login as seller, create a new listing
   - Logout, login as admin
   - Go to "Pending Ads"
   - Approve or decline the listing

5. **Test User Management**:

   - Click "Manage Users" from dashboard
   - Filter by role
   - Change a user's role
   - Verify role update

6. **Test Inspection Oversight**:

   - View all inspections
   - Filter by status
   - Try reassigning an inspector

7. **Test Listing Deletion**:
   - Go to "All Listings"
   - Delete a test listing
   - Confirm deletion

---

## Important Notes

### For Production

1. **Change default passwords** immediately
2. **Enable HTTPS** for admin panel
3. **Add audit logging** for admin actions
4. **Implement rate limiting** on admin endpoints
5. **Regular backups** before admin operations

### For Development

- Admin username: `admin` / `testadmin`
- Default password: `admin123` / `test123`
- All existing cars set to "published"
- Signup form excludes "admin" role

### Limitations

- Only one admin can work on moderation at a time (no locking)
- No undo feature for deletions
- No email notifications for declined ads (manual messages only)
- Charts require manual data refresh (no real-time updates)

---

## Troubleshooting

### "Admin Panel not showing in navbar"

- Verify user role: `python manage.py shell` → `user.role` should be `'admin'`
- Clear browser cache
- Check template rendering: `{% if user.is_admin %}`

### "Permission denied when accessing admin panel"

- Verify `@admin_required` decorator is working
- Check user is authenticated: `user.is_authenticated`
- Verify role: `user.is_admin()` returns `True`

### "Charts not displaying"

- Check Chart.js CDN loaded: View page source, search for "chart.js"
- Check browser console for JavaScript errors
- Verify data is being passed to template context

### "Pending ads not showing"

- Verify car status is "pending": `Car.objects.filter(status='pending')`
- Check migration applied: `python manage.py showmigrations cars`
- Verify query in view: `Car.objects.filter(status="pending")`

---

## Admin Panel File Structure

```
admin_panel/
├── __init__.py
├── apps.py
├── decorators.py          # @admin_required decorator
├── urls.py                # Admin URL patterns
├── views.py               # All admin views
└── templates/admin_panel/
    ├── dashboard.html            # Main dashboard with stats & charts
    ├── pending_ads.html          # Ad moderation list
    ├── decline_ad.html           # Decline form with reason
    ├── user_management.html      # User list & filters
    ├── edit_user_role.html       # Role change form
    ├── delete_user.html          # User deletion confirmation
    ├── inspection_oversight.html # All inspections list
    ├── reassign_inspector.html   # Inspector reassignment
    └── all_listings.html         # Complete car inventory
```

---

## Next Steps / Future Enhancements

1. **Email Notifications**: Send emails to sellers on approve/decline
2. **Audit Log**: Track all admin actions (who did what, when)
3. **Bulk Actions**: Approve/decline multiple ads at once
4. **Advanced Filters**: Date range, price range, seller filtering
5. **Export Reports**: CSV/PDF export of statistics
6. **Real-time Dashboard**: Auto-refresh statistics
7. **Admin Roles**: Super admin vs regular admin permissions
8. **Activity Timeline**: Recent admin actions feed
9. **Dispute Management**: Formal dispute resolution workflow
10. **Performance Metrics**: Response time tracking for inspections

---

## Summary

✅ **Admin role implemented** and protected from public signup  
✅ **Ad moderation system** with pending/published/declined workflow  
✅ **User management** with role editing and deletion  
✅ **Inspection oversight** with reassignment capability  
✅ **Analytics dashboard** with charts matching provided image  
✅ **Listing management** with delete functionality  
✅ **Security decorators** protecting all admin views  
✅ **Database migrations** applied successfully

**Admin Panel Ready for Use!**

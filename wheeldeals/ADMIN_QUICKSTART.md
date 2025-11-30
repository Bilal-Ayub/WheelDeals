# WheelDeals Admin Role - Quick Start Guide

## 🚀 What's New

A complete **Admin Panel** has been added to WheelDeals with:

- ✅ Ad moderation (approve/decline listings)
- ✅ User management (view, edit roles, delete)
- ✅ Inspection oversight (reassign inspectors, view all reports)
- ✅ Analytics dashboard (statistics & charts)
- ✅ Listing management (delete any ad)

---

## 🔑 Creating Your First Admin User

### Quick Method (Copy & Paste)

```bash
# 1. Activate virtual environment
.\my_env\Scripts\Activate.ps1

# 2. Run the creation script
python create_admin.py
```

Follow the prompts or press Enter for defaults:

- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@wheeldeals.com`

### Alternative: Django Shell

```bash
python manage.py shell
```

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
print(f"✅ Admin created: {admin.username}")
```

---

## 📊 Accessing the Admin Panel

1. **Start the server** (if not already running):

   ```bash
   python manage.py runserver
   ```

2. **Login as admin**:

   - Go to: `http://127.0.0.1:8000/users/login/`
   - Username: `admin`
   - Password: `admin123`

3. **Access Admin Panel**:
   - Look for yellow **"Admin Panel"** link in navbar
   - Or go directly to: `http://127.0.0.1:8000/admin-panel/`

---

## 🎯 Key Features

### 1. Dashboard (`/admin-panel/`)

- **Statistics Cards**: Total users, buyers, sellers, inspectors, online users, total ads
- **Charts**: Ads by city (pie chart), Ads by make (bar chart)
- **Pending Requests**: Quick view of ads awaiting approval
- **Quick Actions**: Links to all admin sections

### 2. Pending Ads (`/admin-panel/pending-ads/`)

- View all listings waiting for approval
- **Approve**: Make listing public (status → published)
- **Decline**: Reject listing with reason (status → declined)
- Seller sees decline reason on their listing

### 3. User Management (`/admin-panel/users/`)

- View all users with filtering by role
- Edit any user's role (buyer ↔ seller ↔ inspector ↔ admin)
- Delete user accounts (except your own)
- See join date and last login

### 4. Inspection Oversight (`/admin-panel/inspections/`)

- View all inspection requests (all statuses)
- Filter by: requested, accepted, assigned, in_progress, completed, rejected
- **Reassign inspectors** to different users
- View completed inspection reports
- Monitor inspection workflow

### 5. All Listings (`/admin-panel/all-listings/`)

- View complete car inventory
- Filter by: pending, published, declined
- **Delete any listing** permanently
- See view counts and status

---

## 🔒 Security Features

### What's Protected

- ✅ Admin role **cannot be selected** during signup (hidden from form)
- ✅ All admin views protected by `@admin_required` decorator
- ✅ Non-admin users redirected with error message
- ✅ Admin cannot delete own account

### How It Works

```python
# Only admins can access these pages
@admin_required
def admin_dashboard(request):
    # View code...
```

---

## 📝 How Ad Moderation Works

### New Listing Flow

1. **Seller creates listing** → Status: `pending` (not visible to public)
2. **Admin reviews** → Goes to "Pending Ads"
3. **Admin approves** → Status: `published` (visible on site)
   **OR**
   **Admin declines** → Status: `declined` + reason stored
4. **Seller notification** → Message shows on listing page

### Important Notes

- ⚠️ **New listings default to "pending"** (require admin approval)
- ⚠️ **Only "published" ads appear** in browse/search/home
- ⚠️ **Existing ads were set to "published"** during migration
- ℹ️ Declined ads still visible to seller with reason

---

## 🧪 Testing Checklist

### Quick Test (5 minutes)

1. ✅ Create admin user (using script or shell)
2. ✅ Login and see yellow "Admin Panel" link in navbar
3. ✅ View dashboard with statistics
4. ✅ Login as seller, create a new car listing
5. ✅ Login as admin, see pending ad, approve it
6. ✅ Verify approved ad now appears on home page
7. ✅ Go to "User Management", change a user's role
8. ✅ Go to "Inspections", filter by status
9. ✅ Go to "All Listings", delete a test listing

---

## 📁 Files Created

### Admin App Structure

```
admin_panel/
├── __init__.py
├── apps.py
├── decorators.py              # @admin_required decorator
├── urls.py                    # URL routing
├── views.py                   # All admin views (11 views)
└── templates/admin_panel/
    ├── dashboard.html         # Main dashboard with stats & Chart.js
    ├── pending_ads.html       # Ad moderation list
    ├── decline_ad.html        # Decline form
    ├── user_management.html   # User list
    ├── edit_user_role.html    # Role editor
    ├── delete_user.html       # Delete confirmation
    ├── inspection_oversight.html  # Inspection list
    ├── reassign_inspector.html    # Inspector reassignment
    └── all_listings.html      # Complete inventory
```

### Helper Scripts

- `create_admin.py` - Interactive admin user creation
- `ADMIN_ROLE_GUIDE.md` - Complete documentation

### Database Changes

- `users/migrations/0005_alter_customuser_role.py` - Added "admin" role
- `cars/migrations/0004_car_declined_reason_car_status.py` - Added status field

---

## 🐛 Troubleshooting

### "Admin Panel link not showing"

**Fix**: Verify user role

```python
python manage.py shell
>>> from users.models import CustomUser
>>> user = CustomUser.objects.get(username='YOUR_USERNAME')
>>> user.role
'admin'  # Should show 'admin'
>>> user.is_admin()
True  # Should return True
```

### "Permission denied on admin panel"

**Fix**: Clear browser cache and re-login

### "Pending ads not showing"

**Fix**: Check car status field exists

```python
python manage.py showmigrations cars
```

Should show `[X] 0004_car_declined_reason_car_status`

### "Charts not displaying"

**Fix**: Check browser console (F12) for JavaScript errors. Verify Chart.js CDN loads.

---

## 📚 Documentation Files

- **`ADMIN_ROLE_GUIDE.md`** - Complete technical documentation
- **`ADMIN_QUICKSTART.md`** - This file (quick reference)
- **`INSPECTION_TESTING_ROADMAP.md`** - Testing guide for inspection system
- **`create_admin.py`** - Admin user creation script

---

## 💡 Tips

### For Development

- Default admin credentials: `admin` / `admin123`
- All existing cars are "published" by default
- New listings require admin approval
- Test with multiple roles (buyer, seller, inspector, admin)

### For Production

- ⚠️ **Change default admin password immediately**
- ⚠️ **Use strong passwords** for admin accounts
- ⚠️ **Enable HTTPS** for admin panel
- ⚠️ **Backup database** before bulk deletions
- ⚠️ **Audit admin actions** (consider logging)

---

## 🎓 Admin Responsibilities

### Daily Tasks

1. Review and moderate new listings (pending ads)
2. Monitor inspection request statuses
3. Respond to user management requests
4. Check dashboard for anomalies

### Weekly Tasks

1. Review user activity and roles
2. Clean up declined/old listings
3. Monitor inspection completion rates
4. Review analytics trends

### As Needed

- Reassign inspectors for disputes
- Delete spam/inappropriate listings
- Update user roles (promotions/demotions)
- Resolve inspection disputes

---

## ✅ Implementation Complete!

All admin features are **fully functional** and ready to use:

✅ Admin role added to User model  
✅ Signup form excludes admin role  
✅ Ad moderation system with pending/published/declined workflow  
✅ User management with role editing  
✅ Inspection oversight with reassignment  
✅ Analytics dashboard with Chart.js visualizations  
✅ Listing management with delete capability  
✅ Security decorators on all admin views  
✅ Database migrations applied  
✅ Existing cars updated to "published"

**Ready to test!** 🚀

---

## 📞 Quick Reference

| Feature          | URL                          | Description        |
| ---------------- | ---------------------------- | ------------------ |
| **Dashboard**    | `/admin-panel/`              | Main admin hub     |
| **Pending Ads**  | `/admin-panel/pending-ads/`  | Moderate listings  |
| **Users**        | `/admin-panel/users/`        | Manage users       |
| **Inspections**  | `/admin-panel/inspections/`  | Oversight panel    |
| **All Listings** | `/admin-panel/all-listings/` | Complete inventory |
| **Login**        | `/users/login/`              | Admin login        |

**Server**: `http://127.0.0.1:8000/`  
**Admin Panel**: `http://127.0.0.1:8000/admin-panel/`

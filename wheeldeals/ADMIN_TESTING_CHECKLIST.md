# Admin Role Testing Checklist

Use this checklist to verify all admin features are working correctly.

---

## ✅ Pre-Testing Setup

- [ ] Virtual environment activated: `.\my_env\Scripts\Activate.ps1`
- [ ] Database migrations applied: `python manage.py migrate`
- [ ] Admin user created (Username: `admin`, Password: `admin123`)
- [ ] Development server running: `python manage.py runserver`

**Test at**: `http://127.0.0.1:8000`

---

## 🔐 1. Admin Role Security

### Test 1.1: Admin Role Not in Signup

- [ ] Go to `/users/register/`
- [ ] Check role options (should only see: Buyer, Seller, Inspector)
- [ ] Verify "Admin" is NOT selectable
- [ ] ✅ **PASS**: Admin role hidden from signup

### Test 1.2: Admin Access Control

- [ ] Logout (if logged in)
- [ ] Try to access `/admin-panel/` directly
- [ ] Should redirect to home with error message
- [ ] ✅ **PASS**: Unauthorized access blocked

### Test 1.3: Admin Login

- [ ] Login with: `admin` / `admin123`
- [ ] Yellow "Admin Panel" link appears in navbar
- [ ] Click "Admin Panel" → Dashboard loads
- [ ] ✅ **PASS**: Admin access granted

---

## 📊 2. Admin Dashboard

### Test 2.1: Statistics Cards

- [ ] View dashboard at `/admin-panel/`
- [ ] Verify "Total Users" card shows count
- [ ] Verify "Total Buyers" card shows count
- [ ] Verify "Total Sellers" card shows count
- [ ] Verify "Total Users online" card shows count
- [ ] Verify "Total Ads" card shows count
- [ ] Verify "Approval requests" card shows pending count
- [ ] ✅ **PASS**: All statistics display correctly

### Test 2.2: Charts

- [ ] Verify "Ads Posted by City" pie chart displays
- [ ] Verify "Ads by Make" bar chart displays
- [ ] Check legend shows correctly
- [ ] Hover over chart segments (should show tooltips)
- [ ] ✅ **PASS**: Charts render with Chart.js

### Test 2.3: Quick Actions

- [ ] Click "Pending Ads" button → Redirects to pending ads page
- [ ] Click "Manage Users" button → Redirects to user management
- [ ] Click "Inspections" button → Redirects to inspection oversight
- [ ] Click "All Listings" button → Redirects to all listings
- [ ] ✅ **PASS**: All quick action links work

---

## 🚗 3. Ad Moderation System

### Test 3.1: New Listing Goes to Pending

- [ ] Logout admin, login as seller
- [ ] Create a new car listing (any details)
- [ ] Success message: "Your car listing has been submitted for admin approval!"
- [ ] Logout, login as admin
- [ ] Go to "Pending Ads"
- [ ] Verify new listing appears in pending list
- [ ] ✅ **PASS**: New listings require approval

### Test 3.2: Approve Listing

- [ ] On "Pending Ads" page, find a pending listing
- [ ] Click "Approve" button
- [ ] Confirm action
- [ ] Success message appears
- [ ] Listing disappears from pending list
- [ ] Logout, browse cars as guest → Listing appears in search
- [ ] ✅ **PASS**: Approve functionality works

### Test 3.3: Decline Listing

- [ ] Login as seller, create another listing
- [ ] Login as admin, go to "Pending Ads"
- [ ] Click "Decline" for the listing
- [ ] Enter decline reason: "Test: Incomplete information"
- [ ] Submit form
- [ ] Success message appears
- [ ] Login as seller, view your listings
- [ ] Declined listing shows decline reason
- [ ] ✅ **PASS**: Decline functionality works

### Test 3.4: Public Visibility

- [ ] Logout (browse as guest)
- [ ] Go to home page and "Browse Cars"
- [ ] Only "published" listings appear
- [ ] "Pending" and "declined" listings hidden
- [ ] ✅ **PASS**: Only published ads visible to public

---

## 👥 4. User Management

### Test 4.1: View All Users

- [ ] Login as admin
- [ ] Go to `/admin-panel/users/`
- [ ] All users displayed in table
- [ ] Shows: ID, username, name, email, role, city, joined date, last login
- [ ] ✅ **PASS**: User list displays correctly

### Test 4.2: Filter by Role

- [ ] On user management page, click "Buyers" filter
- [ ] Only buyer users displayed
- [ ] Click "Sellers" → Only sellers shown
- [ ] Click "Inspectors" → Only inspectors shown
- [ ] Click "Admins" → Only admins shown
- [ ] Click "All Users" → All users shown
- [ ] ✅ **PASS**: Role filtering works

### Test 4.3: Edit User Role

- [ ] Click "Edit Role" for a buyer user
- [ ] Change role to "Seller"
- [ ] Submit form
- [ ] Success message appears
- [ ] User's role badge updated in list
- [ ] ✅ **PASS**: Role editing works

### Test 4.4: Delete User

- [ ] Click "Delete" for a non-admin user
- [ ] Confirmation page appears
- [ ] Confirm deletion
- [ ] Success message appears
- [ ] User removed from list
- [ ] ✅ **PASS**: User deletion works

### Test 4.5: Self-Deletion Prevention

- [ ] Try to delete your own admin account
- [ ] "Delete" button should not appear for your user
- [ ] OR error message: "You cannot delete your own account"
- [ ] ✅ **PASS**: Self-deletion blocked

---

## 🔍 5. Inspection Oversight

### Test 5.1: View All Inspections

- [ ] Go to `/admin-panel/inspections/`
- [ ] All inspection requests displayed
- [ ] Shows: ID, car, buyer, seller, inspector, status, dates
- [ ] ✅ **PASS**: Inspection list displays

### Test 5.2: Filter by Status

- [ ] Click "Requested" filter → Only requested inspections shown
- [ ] Click "Accepted" → Only accepted shown
- [ ] Click "Assigned" → Only assigned shown
- [ ] Click "In Progress" → Only in-progress shown
- [ ] Click "Completed" → Only completed shown
- [ ] Click "Rejected" → Only rejected shown
- [ ] Click "All" → All inspections shown
- [ ] ✅ **PASS**: Status filtering works

### Test 5.3: Reassign Inspector

- [ ] Find an inspection with status "assigned" or "in_progress"
- [ ] Click "Reassign" button
- [ ] Select a different inspector from dropdown
- [ ] Submit form
- [ ] Success message appears
- [ ] Inspector name updated in list
- [ ] ✅ **PASS**: Inspector reassignment works

### Test 5.4: View Completed Reports

- [ ] Find a completed inspection
- [ ] Click "View Report" button
- [ ] Opens full inspection report in new tab
- [ ] All details visible
- [ ] ✅ **PASS**: Report viewing works

---

## 📋 6. All Listings Management

### Test 6.1: View All Listings

- [ ] Go to `/admin-panel/all-listings/`
- [ ] All car listings displayed (all statuses)
- [ ] Shows: ID, image, details, seller, price, status, posted date, views
- [ ] ✅ **PASS**: Listing inventory displays

### Test 6.2: Filter by Status

- [ ] Click "Pending" filter → Only pending listings
- [ ] Click "Published" → Only published listings
- [ ] Click "Declined" → Only declined listings
- [ ] Click "All" → All listings
- [ ] ✅ **PASS**: Status filtering works

### Test 6.3: Delete Listing

- [ ] Click "Delete" button for any listing
- [ ] Confirm deletion
- [ ] Success message appears
- [ ] Listing removed from database
- [ ] Verify listing no longer appears in browse/search
- [ ] ✅ **PASS**: Listing deletion works

### Test 6.4: View Listing Details

- [ ] Click "View" button for a listing
- [ ] Opens car detail page in new tab
- [ ] Shows full car information
- [ ] ✅ **PASS**: Listing preview works

---

## 🎨 7. UI/UX Testing

### Test 7.1: Responsive Design

- [ ] Resize browser window (mobile, tablet, desktop sizes)
- [ ] Dashboard cards stack properly on mobile
- [ ] Tables scroll horizontally on small screens
- [ ] Charts resize appropriately
- [ ] Navigation menu collapses on mobile
- [ ] ✅ **PASS**: Responsive design works

### Test 7.2: Navigation

- [ ] "Admin Panel" link visible only when logged in as admin
- [ ] Navbar shows user role indicator
- [ ] All admin pages have "Back to Dashboard" button
- [ ] Breadcrumb navigation clear
- [ ] ✅ **PASS**: Navigation intuitive

### Test 7.3: Messages & Feedback

- [ ] Success messages appear after actions (green)
- [ ] Error messages appear for invalid actions (red)
- [ ] Confirmation dialogs for destructive actions (delete)
- [ ] Form validation errors display clearly
- [ ] ✅ **PASS**: User feedback clear

---

## 🔄 8. Integration Testing

### Test 8.1: Admin + Seller Workflow

- [ ] Login as seller, create listing (goes to pending)
- [ ] Login as admin, approve listing
- [ ] Login as seller, verify listing now published
- [ ] Seller can edit/delete own listing
- [ ] ✅ **PASS**: Seller workflow integrates

### Test 8.2: Admin + Buyer Workflow

- [ ] Login as buyer, browse cars
- [ ] Only published cars visible
- [ ] Request inspection on published car
- [ ] Login as admin, view inspection in oversight panel
- [ ] Verify inspection details correct
- [ ] ✅ **PASS**: Buyer workflow integrates

### Test 8.3: Admin + Inspector Workflow

- [ ] Create inspection request (buyer → seller → accepted)
- [ ] Login as inspector, assign self to inspection
- [ ] Login as admin, reassign to different inspector
- [ ] Login as different inspector, verify reassignment
- [ ] Complete inspection
- [ ] Login as admin, view completed report
- [ ] ✅ **PASS**: Inspector workflow integrates

---

## 🛡️ 9. Security Testing

### Test 9.1: URL Direct Access (Unauthorized)

- [ ] Logout completely
- [ ] Try to access: `/admin-panel/` → Blocked
- [ ] Try to access: `/admin-panel/users/` → Blocked
- [ ] Try to access: `/admin-panel/pending-ads/` → Blocked
- [ ] All redirect to home with error message
- [ ] ✅ **PASS**: Direct URL access blocked

### Test 9.2: URL Direct Access (Non-Admin User)

- [ ] Login as buyer (not admin)
- [ ] Try to access: `/admin-panel/` → Blocked
- [ ] Error message: "You do not have permission"
- [ ] Redirected to home page
- [ ] ✅ **PASS**: Non-admin users blocked

### Test 9.3: CSRF Protection

- [ ] All forms have `{% csrf_token %}`
- [ ] Submit form without CSRF → Rejected
- [ ] ✅ **PASS**: CSRF protection active

---

## 📈 10. Performance Testing

### Test 10.1: Dashboard Load Time

- [ ] Dashboard loads in < 2 seconds
- [ ] Statistics calculated efficiently
- [ ] Charts render smoothly
- [ ] No lag on interaction
- [ ] ✅ **PASS**: Dashboard performs well

### Test 10.2: Large Data Sets

- [ ] Create 20+ listings
- [ ] Create 10+ users
- [ ] Dashboard still loads quickly
- [ ] Tables paginate or scroll smoothly
- [ ] Filters respond quickly
- [ ] ✅ **PASS**: Handles large datasets

---

## 🎯 Final Checklist

### Core Features

- [ ] ✅ Admin role created and protected
- [ ] ✅ Ad moderation (pending → published/declined)
- [ ] ✅ User management (view, edit, delete)
- [ ] ✅ Inspection oversight (view all, reassign)
- [ ] ✅ Analytics dashboard (stats + charts)
- [ ] ✅ Listing management (view all, delete)

### Security

- [ ] ✅ Admin role not in signup
- [ ] ✅ @admin_required decorator working
- [ ] ✅ Unauthorized access blocked
- [ ] ✅ Self-deletion prevented

### UI/UX

- [ ] ✅ Responsive design
- [ ] ✅ Clear navigation
- [ ] ✅ User feedback messages
- [ ] ✅ Charts display correctly

### Integration

- [ ] ✅ Works with seller workflow
- [ ] ✅ Works with buyer workflow
- [ ] ✅ Works with inspector workflow
- [ ] ✅ All features interconnected

---

## 📝 Test Results Summary

**Date**: **********\_**********  
**Tester**: **********\_**********  
**Browser**: **********\_**********  
**OS**: **********\_**********

### Results

- **Total Tests**: 45+
- **Passed**: **\_** / 45
- **Failed**: **\_** / 45
- **Skipped**: **\_** / 45

### Issues Found

1. ***
2. ***
3. ***

### Notes

---

---

---

---

## ✅ Sign-Off

**All tests passed?** [ ] YES [ ] NO

**Ready for production?** [ ] YES [ ] NO

**Signature**: **********\_**********  
**Date**: **********\_**********

---

**Total Estimated Testing Time**: 30-45 minutes

**Quick Test (Essential Only)**: 10-15 minutes

- Test 1.3 (Admin login)
- Test 2.1 (Dashboard stats)
- Test 3.1-3.2 (Ad moderation)
- Test 4.1 (User management)
- Test 5.1 (Inspections)
- Test 6.3 (Delete listing)

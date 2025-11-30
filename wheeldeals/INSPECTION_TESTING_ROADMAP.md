# Inspection System Testing Roadmap

## Prerequisites

- Server running: `python manage.py runserver`
- At least 3 test users:
  - **Buyer** (role: buyer)
  - **Seller** (role: seller) with at least 1 car listed
  - **Inspector** (role: inspector)
- **Guest** (no login)

---

## Phase 1: Inspection Request Workflow

### Test 1.1: Buyer Requests Inspection

**User:** Buyer  
**Steps:**

1. Login as buyer
2. Navigate to any car listing (owned by another user)
3. Click "Request Inspection" button
4. Verify success message appears
5. Navigate to "My Inspection Requests" (add `/inspections/buyer/status/` to URL)
6. Verify request appears with status "Requested"
7. Note the Inspection ID (format: INS-YYYYMMDD-XXXXX)

**Expected Results:**
✅ Request created with status "requested"  
✅ Inspection ID auto-generated  
✅ Payment cost shows $50  
✅ Request visible in buyer's dashboard

---

### Test 1.2: 30-Day Cooldown Enforcement

**User:** Same Buyer  
**Steps:**

1. Stay logged in as buyer
2. Try to click "Request Inspection" on the same car again
3. Verify error message appears

**Expected Results:**
✅ Error: "You have already requested an inspection for this car within the last 30 days"  
✅ Button should show cooldown message or be disabled

---

### Test 1.3: Seller Views Pending Requests

**User:** Seller (car owner)  
**Steps:**

1. Logout and login as seller
2. Navigate to "Inspection Requests" (add `/inspections/seller/requests/` to URL)
3. Verify pending inspection request appears
4. Note the request details: buyer name, car, status

**Expected Results:**
✅ Pending request visible  
✅ Shows "Requested" status  
✅ Two action buttons: "Accept" and "Reject"

---

### Test 1.4: Seller Rejects Request

**User:** Seller  
**Steps:**

1. Stay on seller's inspection requests page
2. Click "Reject" button on a request
3. Enter rejection reason: "Vehicle not available for inspection"
4. Submit form
5. Verify request status changes to "Rejected"

**Expected Results:**
✅ Status changes to "rejected"  
✅ Rejection reason saved  
✅ Buyer can see rejection reason in their dashboard

---

### Test 1.5: Seller Accepts and Schedules Inspection

**User:** Seller  
**Steps:**

1. Create a NEW inspection request (as buyer for a different car)
2. Login as seller
3. Navigate to "Inspection Requests"
4. Click "Accept" button
5. Select a future date (at least tomorrow or later)
6. Select time slot (9 AM - 12 PM, 12 PM - 3 PM, or 3 PM - 6 PM)
7. Submit form

**Expected Results:**
✅ Status changes to "accepted"  
✅ Scheduled date and time saved  
✅ Cost fixed at $50  
✅ Request appears in inspector dashboard for assignment

---

### Test 1.6: Inspector Views Unassigned Requests

**User:** Inspector  
**Steps:**

1. Logout and login as inspector
2. Navigate to "Inspector Dashboard" (add `/inspections/inspector/dashboard/` to URL)
3. View "Unassigned Inspections" section
4. Verify accepted inspection appears

**Expected Results:**
✅ Accepted inspection visible  
✅ Shows car details, scheduled date/time  
✅ "Assign to Me" button available

---

### Test 1.7: Inspector Self-Assigns Inspection

**User:** Inspector  
**Steps:**

1. Stay on inspector dashboard
2. Click "Assign to Me" button for an unassigned inspection
3. Verify success message
4. Check "My Assigned Inspections" section

**Expected Results:**
✅ Status changes to "assigned"  
✅ Inspector name recorded  
✅ Inspection moves from "Unassigned" to "My Assigned" section  
✅ "Start Inspection" button appears

---

### Test 1.8: Inspector Starts Inspection

**User:** Inspector  
**Steps:**

1. Stay on inspector dashboard
2. In "My Assigned Inspections" section, click "Start Inspection"
3. Verify success message
4. Check status changes

**Expected Results:**
✅ Status changes to "in_progress"  
✅ "Submit Report" button appears  
✅ Inspection remains in "My Assigned Inspections" section

---

## Phase 2: Inspector Report Submission

### Test 2.1: Submit Complete Inspection Report

**User:** Inspector  
**Steps:**

1. Stay logged in as inspector
2. On dashboard, click "Submit Report" for an in-progress inspection
3. Fill out all 14 component ratings (select 1-5 for each):
   - **Exterior:** Paint, Body, Glass/Windows, Lights/Signals
   - **Tires & Wheels:** Tire Condition, Wheel Condition
   - **Mechanical:** Engine, Transmission, Brakes, Suspension
   - **Interior:** Interior Condition, Seats/Upholstery, Dashboard/Controls
   - **Electronics:** Electronics
4. Add overall comments: "Vehicle is in good condition overall. Minor wear on seats."
5. Upload 2-3 inspection photos with captions
6. Submit form

**Expected Results:**
✅ Report saved successfully  
✅ Status changes to "completed"  
✅ Average rating calculated from 14 components  
✅ Photos uploaded and linked to report  
✅ Completed date recorded

---

### Test 2.2: Verify Report Components (14 Total)

**User:** Inspector  
**Steps:**

1. After submission, navigate back to dashboard
2. Click "View Report" for the completed inspection
3. Verify all components are displayed

**Expected Results:**
✅ All 14 components visible  
✅ NO "Rust/Corrosion" field (removed)  
✅ NO "Recommendation" field (removed)  
✅ Average rating displayed correctly  
✅ Formula: Sum of all 14 ratings ÷ 14

---

### Test 2.3: View Report as Buyer

**User:** Buyer (who requested the inspection)  
**Steps:**

1. Login as buyer
2. Navigate to "My Inspection Requests"
3. Find completed inspection
4. Click "View Report" button

**Expected Results:**
✅ Full report visible  
✅ All 14 component ratings displayed  
✅ Inspector name shown  
✅ Inspection photos displayed in grid  
✅ Overall comments visible  
✅ Average rating shown

---

### Test 2.4: View Report as Seller

**User:** Seller (car owner)  
**Steps:**

1. Login as seller
2. Navigate to "Inspection Requests"
3. Find completed inspection
4. Click "View Report" button

**Expected Results:**
✅ Same as buyer view  
✅ Full access to all report details

---

### Test 2.5: Verify Photo Upload (Multiple Photos)

**User:** Inspector  
**Steps:**

1. Submit a new report with 5+ photos
2. Add unique captions for each photo
3. Submit and view report

**Expected Results:**
✅ All photos uploaded successfully  
✅ Captions saved  
✅ Photos displayed in grid layout  
✅ Maximum 10 photos allowed per report

---

## Phase 3: Public Report Display on Listings

### Test 3.1: View Inspection Reports as Guest (No Login)

**User:** Guest  
**Steps:**

1. Logout (or use incognito/private browser)
2. Navigate to a car listing that has completed inspections
3. Scroll down to "Professional Inspection Reports" section

**Expected Results:**
✅ Inspection reports section visible  
✅ Shows count: "Professional Inspection Reports (X)"  
✅ Inspector name displayed  
✅ Average rating displayed (X.X out of 5.0)  
✅ Star rating visualization shown  
✅ 8 key component ratings listed  
✅ First 3 inspection photos displayed  
✅ "View Full Report" button available

---

### Test 3.2: View Multiple Reports on Same Listing

**User:** Guest  
**Steps:**

1. Create 2-3 completed inspections for the same car (using different buyers)
2. View the car listing as guest
3. Verify all reports are displayed

**Expected Results:**
✅ All completed inspections shown  
✅ Each report in separate card  
✅ Reports sorted by completion date (newest first)  
✅ Each shows unique Inspection ID  
✅ Each shows different inspector name (if different)

---

### Test 3.3: Click "View Full Report" from Listing

**User:** Guest  
**Steps:**

1. On car listing page, click "View Full Report" button
2. Verify redirects to full report page

**Expected Results:**
✅ Redirects to `/inspections/report/<inspection_id>/`  
✅ Full report accessible to guests  
✅ All 14 components visible  
✅ All photos visible  
✅ Comments visible

---

### Test 3.4: Verify Reports NOT Shown on Listings Without Inspections

**User:** Guest  
**Steps:**

1. Navigate to a car listing with NO completed inspections
2. Scroll down page

**Expected Results:**
✅ "Professional Inspection Reports" section NOT displayed  
✅ Clean layout with no empty sections  
✅ "Request Inspection" button still visible (if logged in as buyer)

---

### Test 3.5: View Report Display as Logged-In Buyer

**User:** Buyer  
**Steps:**

1. Login as buyer
2. Navigate to any car listing with completed inspections
3. Verify inspection reports section

**Expected Results:**
✅ Same display as guest view  
✅ Inspector name visible  
✅ Average rating visible  
✅ Photos visible  
✅ "View Full Report" button works  
✅ "Request Inspection" button also available (if eligible)

---

## Edge Cases & Integration Tests

### Test 4.1: Rejection Flow

**Steps:**

1. Buyer requests inspection
2. Seller rejects with reason
3. Buyer views status

**Expected Results:**
✅ Status shows "Rejected"  
✅ Rejection reason visible to buyer  
✅ Request NOT visible to inspectors  
✅ Buyer CAN request again on same car (rejection doesn't trigger cooldown)

---

### Test 4.2: Multiple Concurrent Requests

**Steps:**

1. Have 3 different buyers request inspection for same car
2. Seller accepts all 3
3. Different inspectors assign themselves

**Expected Results:**
✅ All 3 requests processed independently  
✅ Each has unique Inspection ID  
✅ Each can be completed separately  
✅ All 3 reports show on car listing after completion

---

### Test 4.3: Inspector Dashboard Organization

**User:** Inspector  
**Steps:**

1. Create 5+ inspection requests
2. Assign 2 to inspector
3. Complete 1
4. View inspector dashboard

**Expected Results:**
✅ "Unassigned Inspections" shows 3 unassigned  
✅ "My Assigned Inspections" shows 1 in-progress  
✅ Completed inspection removed from dashboard  
✅ Each section clearly labeled

---

### Test 4.4: Average Rating Calculation

**User:** Inspector  
**Steps:**

1. Submit report with specific ratings:
   - 10 components at rating 5
   - 4 components at rating 3
2. Calculate expected average: (50 + 12) ÷ 14 = 4.43
3. View report

**Expected Results:**
✅ Average displays as 4.4 (rounded to 1 decimal)  
✅ Star rating shows 4 stars (rounded to nearest whole)  
✅ Calculation based on 14 components only

---

### Test 4.5: Photo Display Limits

**Steps:**

1. Upload 10 photos to inspection report
2. View report on car listing (Phase 3)
3. Click "View Full Report"

**Expected Results:**
✅ Car listing shows only first 3 photos  
✅ Shows "+7 more photos in full report" message  
✅ Full report page shows all 10 photos  
✅ Photos display in responsive grid

---

## Checklist Summary

### Phase 1 Checklist ✓

- [ ] Buyer can request inspection
- [ ] 30-day cooldown enforced
- [ ] Seller sees pending requests
- [ ] Seller can reject with reason
- [ ] Seller can accept and schedule
- [ ] Inspector sees unassigned requests
- [ ] Inspector can self-assign
- [ ] Inspector can start inspection
- [ ] Status transitions work correctly

### Phase 2 Checklist ✓

- [ ] Inspector can submit report with 14 components
- [ ] Photo upload works (multiple photos)
- [ ] Average rating calculated correctly
- [ ] Buyer can view completed report
- [ ] Seller can view completed report
- [ ] Inspector can view submitted report
- [ ] No rust/corrosion field present
- [ ] No recommendation field present

### Phase 3 Checklist ✓

- [ ] Reports visible on car listings (all users)
- [ ] Inspector name displayed publicly
- [ ] Average rating displayed with stars
- [ ] Component ratings summary shown (8 key components)
- [ ] First 3 photos displayed
- [ ] "View Full Report" button works
- [ ] Multiple reports display correctly
- [ ] No reports section hidden when no inspections
- [ ] Guest access works without login

---

## Quick Test Data Setup

```python
# Django shell: python manage.py shell

from users.models import User
from cars.models import Car

# Create test users
buyer = User.objects.create_user(username='testbuyer', password='pass123', role='buyer', first_name='John', last_name='Buyer')
seller = User.objects.create_user(username='testseller', password='pass123', role='seller', first_name='Jane', last_name='Seller')
inspector = User.objects.create_user(username='testinspector', password='pass123', role='inspector', first_name='Mike', last_name='Inspector')

# Create test car
car = Car.objects.create(
    seller=seller,
    make='Toyota',
    model='Camry',
    year=2020,
    price=25000,
    mileage=30000,
    description='Well maintained sedan'
)

print(f"Buyer: testbuyer / pass123")
print(f"Seller: testseller / pass123")
print(f"Inspector: testinspector / pass123")
print(f"Car ID: {car.id}")
```

---

## URL Reference

- Car Listings: `/cars/`
- Car Detail: `/cars/<car_id>/`
- Request Inspection: `/inspections/request/<car_id>/` (POST)
- Buyer Status: `/inspections/buyer/status/`
- Seller Requests: `/inspections/seller/requests/`
- Accept Inspection: `/inspections/accept/<inspection_id>/`
- Reject Inspection: `/inspections/reject/<inspection_id>/`
- Inspector Dashboard: `/inspections/inspector/dashboard/`
- Assign Inspection: `/inspections/assign/<inspection_id>/`
- Start Inspection: `/inspections/start/<inspection_id>/`
- Submit Report: `/inspections/submit-report/<inspection_id>/`
- View Report: `/inspections/report/<inspection_id>/`

---

## Notes

- Test in order: Phase 1 → Phase 2 → Phase 3
- Each phase depends on previous phases working
- Use browser dev tools (F12) to check for JavaScript errors
- Check Django debug toolbar for database query optimization
- Verify no N+1 query issues on car listing page
- Test responsive design on mobile viewport

**Estimated Testing Time:** 45-60 minutes for complete testing

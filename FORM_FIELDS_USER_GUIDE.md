# 📖 Form Fields - User Guide

## How to Use the Fixed Forms

This guide explains how the new dropdown-based forms work and what options are available.

---

## 👤 Edit Your Profile Form

**Location:** Dashboard → Edit Profile

### Personal Information Section

#### Name

- **Type:** Text input
- **What to enter:** Your full name
- **Example:** John Doe
- **Validation:** Required field

#### Email

- **Type:** Email input
- **What to enter:** Your email address
- **Example:** john@example.com
- **Validation:** Must be valid email format

---

### Eligibility Information Section

#### Age ⭐ **NEW - Now a Dropdown**

- **Type:** Select dropdown
- **Options:**
  - Select Age (please choose)
  - 18-25 years
  - 26-35 years
  - 36-45 years
  - 46-55 years
  - 56-65 years
  - 65 years and above
- **How to use:** Click dropdown, select your age range
- **Why?** Better privacy, consistent data

**Example Usage:**

```
If you are 28 years old → Select "26-35 years"
If you are 32 years old → Select "26-35 years"
If you are 70 years old → Select "65 years and above"
```

#### Caste ⭐ **Now a Dropdown**

- **Type:** Select dropdown
- **Options:**
  - (blank - select one)
  - General (G)
  - Other Backward Caste (OBC)
  - Particularly Vulnerable Tribal Group (PVTG)
  - Scheduled Class (SC)
  - Scheduled Tribe (ST)
- **How to use:** Click dropdown, select your caste category
- **Important:** Official government categories

#### Marital Status ⭐ **Now a Dropdown**

- **Type:** Select dropdown
- **Options:**
  - (blank - select one)
  - Married
  - Never Married
  - Widowed
  - Divorcee
- **How to use:** Click dropdown, select your status

#### Income

- **Type:** Number input
- **What to enter:** Your annual income in rupees
- **Example:** 500000 (for ₹5 lakhs)
- **Range:** Positive numbers only

---

### Status Information Section

#### Gender ⭐ **Now a Dropdown**

- **Type:** Select dropdown
- **Options:**
  - (blank - select one)
  - Male (M)
  - Female (F)
  - Transgender (T)
- **How to use:** Click dropdown, select your gender

#### Location ⭐ **Now a Dropdown**

- **Type:** Select dropdown
- **Options:**
  - (blank - select one)
  - Rural
  - Urban
- **How to use:** Click dropdown, select location type
- **Definition:**
  - Rural = Non-urban areas, villages, countryside
  - Urban = City, town, metropolitan areas

#### Disability ⭐ **Now a Dropdown**

- **Type:** Select dropdown
- **Options:**
  - Select (none selected)
  - Yes (Person with disability)
  - No (Not a person with disability)
- **How to use:** Click dropdown, select Yes or No
- **Note:** Used to match disability-specific schemes

#### Minority ⭐ **Now a Dropdown**

- **Type:** Select dropdown
- **Options:**
  - Select (none selected)
  - Yes (Minority community member)
  - No (Not from minority community)
- **How to use:** Click dropdown, select Yes or No

#### Below Poverty Line ⭐ **Now a Dropdown**

- **Type:** Select dropdown
- **Options:**
  - Select (none selected)
  - Yes (BPL household)
  - No (APL household)
- **How to use:** Click dropdown, select Yes or No
- **Definition:**
  - BPL = Below Poverty Line (eligible for BPL schemes)
  - APL = Above Poverty Line (not eligible for BPL-only schemes)

---

## 🔍 Advanced Search Form

**Location:** Home → Search Schemes → Advanced Search

### Available Filter Fields

#### Age Range ⭐ **NEW - Now a Dropdown**

- **Options:** Same 6 age ranges as profile
- **Use case:** Find schemes matching your age group
- **Default:** (leave empty to see all)

#### Income Range ⭐ **Now a Dropdown**

- **Options:**
  - (leave empty for any income)
  - ₹0 - ₹1 Lakh
  - ₹1 Lakh - ₹3 Lakh
  - ₹3 Lakh - ₹5 Lakh
  - ₹5 Lakh - ₹10 Lakh
  - Above ₹10 Lakh
- **Use case:** Find schemes matching your income level

#### Gender

- **Options:** Male, Female, Transgender
- **Use case:** Find gender-specific schemes

#### Location

- **Options:** Rural, Urban, All
- **Use case:** Find location-specific schemes

#### Caste

- **Options:** All 5 caste categories
- **Use case:** Find caste-specific schemes

#### Disability

- **Options:** Yes, No, All
- **Use case:** Find disability-specific schemes

#### Minority Status

- **Options:** Yes, No, All
- **Use case:** Find minority-specific schemes

#### Below Poverty Line

- **Options:** Yes, No, All
- **Use case:** Find BPL-specific schemes

---

## 📋 Add/Edit Scheme Form (Admin Only)

**Location:** Admin Dashboard → Manage Schemes

### Age Range Fields ⭐ **Now Dropdowns**

#### Minimum Age

- **Type:** Select dropdown
- **Options:** 18, 19, 20, ... 75
- **Purpose:** Minimum age requirement for scheme
- **Example:** If minimum is 25, users 25 and above can apply

#### Maximum Age

- **Type:** Select dropdown
- **Options:** 18, 19, 20, ... 75
- **Purpose:** Maximum age limit for scheme
- **Example:** If maximum is 60, users up to age 60 can apply

### Category Fields ⭐ **Now Dropdowns**

#### Gender

- **Type:** Select dropdown
- **Options:** Leave blank (any), Male, Female, Transgender

#### Marital Status

- **Type:** Select dropdown
- **Options:** Leave blank (any), Married, Never Married, Widowed, Divorcee

#### Caste

- **Type:** Select dropdown
- **Options:** Leave blank (any), or select specific category

#### Location

- **Type:** Select dropdown
- **Options:** Leave blank (any), Rural, Urban

#### Status Flags ⭐ **Now Dropdowns**

**Disability:**

- Any (no requirement)
- Yes (scheme for persons with disability)
- No (scheme for non-disabled)

**Minority:**

- Any (no requirement)
- Yes (scheme for minority community)
- No (scheme for non-minority)

**Below Poverty Line:**

- Any (no requirement)
- Yes (scheme for BPL households)
- No (scheme for APL households)

---

## ✅ Best Practices

### When Filling Your Profile:

1. **Be Honest**
   - Select age range that includes your age
   - Select correct caste category
   - Select correct marital status

2. **Complete All Required Fields**
   - Required fields marked with \*
   - Leave optional fields blank if not applicable

3. **Double-Check Before Saving**
   - Verify all selections are correct
   - Check age range matches your actual age
   - Ensure income is entered correctly

4. **Update When Changes Happen**
   - Update marital status if changed
   - Update income if it increases significantly
   - Update disability/minority status if applicable

---

## ❓ FAQ

### Q: What if my age is exactly at the boundary?

**A:** Select the range that includes your age.

- Age 25: Select "18-25 years"
- Age 26: Select "26-35 years"

### Q: Why is age in ranges instead of exact number?

**A:**

- Better privacy (exact age not stored)
- Still accurate for eligibility matching
- Easier for users
- Standard practice in government forms

### Q: What if I'm unsure about my caste category?

**A:**

- Select "General" if none of the others apply
- Ask at the help desk
- Refer to your government ID
- Contact support

### Q: Can I change my profile later?

**A:** Yes! Go to Dashboard → Edit Profile anytime.

### Q: What if I select wrong information?

**A:** You can edit your profile anytime. Simply:

1. Go to Edit Profile
2. Change the fields
3. Save

### Q: How does age range help with eligibility?

**A:**

- System calculates midpoint of your range
- Compares against scheme min/max age
- Shows if you're eligible

### Q: Do my selections affect privacy?

**A:**

- Age ranges are more private than exact age
- Your data is encrypted
- Information used only for scheme matching
- Never shared without consent

---

## 🎯 Quick Reference

### What Changed?

| Field          | Before      | After                    |
| -------------- | ----------- | ------------------------ |
| Age            | Type number | Select from 6 ranges     |
| Gender         | Type text   | Select from 3 options    |
| Caste          | Type text   | Select from 5 categories |
| Marital Status | Type text   | Select from 4 options    |
| Location       | Type text   | Select from 2 options    |
| Disability     | Type yes/no | Select Yes/No            |
| Minority       | Type yes/no | Select Yes/No            |
| BPL Status     | Type yes/no | Select Yes/No            |

### Why Changed?

- ✅ Better data quality
- ✅ No invalid entries
- ✅ Consistent data
- ✅ Accurate eligibility
- ✅ Faster to fill
- ✅ Mobile-friendly

---

## 🚀 Using the New Forms

### Step 1: Navigate to Form

```
Dashboard → Edit Profile
OR
Home → Advanced Search
```

### Step 2: Click on Dropdown Field

```
See colored field with ▼ arrow
Click to see options
```

### Step 3: Select Option

```
Click option from list
Option is now selected
```

### Step 4: Proceed

```
Fill other required fields
Click Save (for profile)
Click Search (for search form)
```

---

## 💡 Tips

1. **Mobile Users:** Dropdowns work great on touch screens - just tap and select

2. **Keyboard Users:** Use arrow keys to navigate, Enter to select

3. **Accessibility:** All fields have proper labels and descriptions

4. **Dark Mode:** Forms work perfectly in dark mode too

5. **Error Handling:** If required field is missed, clear message shown

---

## 📞 Need Help?

- **Technical Issues?** Contact IT Support
- **Form Questions?** Click help icon next to field
- **Eligibility Questions?** Check our eligibility guide
- **Profile Issues?** Email: support@govaid.gov.in

---

## ✨ Enjoy Using the New Forms!

The updated forms are:

- **Faster** - Select instead of type
- **Easier** - No spelling mistakes
- **Clearer** - Obvious options
- **Better** - More accurate scheme matches

Thank you for using GovAid! 🙏

---

_Last Updated: February 4, 2026_
_Version: 2.1 (Form Fields Update)_

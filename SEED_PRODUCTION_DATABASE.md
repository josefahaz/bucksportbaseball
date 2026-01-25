# Seed Production Database with Inventory

## Problem
The production database on Render only has 41 items (from the old seed_inventory.py script). 
It's missing all pants, jerseys, and the new items from the PDF orders.

## Solution
Run the new seeding script on the Render production server to populate all 125 inventory items.

---

## Steps to Seed Production Database

### 1. Wait for Deployment
After pushing the latest code, wait 2-3 minutes for Render to automatically deploy the new code.

### 2. Access Render Shell
1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Sign in to your account
3. Click on your **bucksport-api** service
4. Click the **"Shell"** tab at the top

### 3. Run the Seeding Script
In the Render shell, type this command:

```bash
python seed_production_inventory.py
```

### 4. Confirm the Import
When prompted, type `yes` to clear existing items and import all 125 items.

You should see output like:
```
============================================================
PRODUCTION INVENTORY SEEDING
============================================================
Running in PRODUCTION mode (PostgreSQL)
✓ Database initialized
✓ Found CSV file: /opt/render/project/src/inventory_upload.csv

WARNING: Database already has 41 items
Clear existing items and re-import? (yes/no): yes
✓ Cleared 41 existing items

Importing items from CSV...
✓ Successfully imported 125 items!

Verifying import...
  - Pants items: 11
  - Jersey items: 25
  - Baseball items: 11
  - Softball items: 26
  - Shared items: 88

✓ TOTAL ITEMS IN DATABASE: 125
============================================================
SEEDING COMPLETE!
============================================================
```

### 5. Verify on Website
1. Go to your production site inventory page
2. Filter by "pants" category
3. You should now see 11 pants items with various sizes
4. Total items should show 125

---

## What Gets Imported

**125 Total Items Including:**
- 11 pants items (Youth XL, Size 30, Youth S/XS, Medium, Girls S/M/L, Womens M/XL)
- 25 jersey items (various sizes and styles)
- All balls, bats, helmets, gloves, cleats
- All softball and baseball equipment
- 10 new items from October & November 2025 PDF orders:
  - 24x PHINIX 12" Safety Softballs
  - 2x Rawlings Catcher's Helmets
  - 1x Easton Youth Catcher's Set
  - 2x Equipment Duffle Bags
  - 4x Lineup Card Sets
  - 3x Portable Batting Tees
  - 25x Ice Cold Packs
  - 1x Softball Pitching Mat
  - 3x Dugout Organizers
  - 1x 6 Gallon Bucket

---

## Troubleshooting

**If the shell command doesn't work:**
Try running from the bucksport_api directory:
```bash
cd bucksport_api
python seed_production_inventory.py
```

**If you get a "file not found" error:**
The CSV file should be at the root level. Try:
```bash
cd ..
python bucksport_api/seed_production_inventory.py
```

**If you need to re-run:**
The script will ask for confirmation before clearing existing data, so it's safe to run multiple times.

---

## Alternative: Manual Database Reset

If the shell method doesn't work, you can also:
1. In Render dashboard, go to your PostgreSQL database
2. Delete and recreate the database
3. Redeploy the service (it will auto-run migrations)
4. Then run the seed script

---

## After Seeding

Once complete, your production inventory will have:
- ✅ All 125 items from inventory_upload.csv
- ✅ All pants with sizes visible
- ✅ All jerseys with sizes visible
- ✅ Items from PDF orders included
- ✅ Proper categorization (jersey, pants, ball, bat, etc.)
- ✅ Proper division assignment (Baseball, Softball, Shared)

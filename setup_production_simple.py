"""
Simplified production setup - manually set your DATABASE_URL here.
"""
import os
import sys

# INSTRUCTIONS:
# 1. Go to https://dashboard.render.com
# 2. Click on your PostgreSQL database (should be named something like "bucksport-db")
# 3. Scroll down to "Connections" section
# 4. Copy the "Internal Database URL" 
# 5. Paste it below between the quotes

# PASTE YOUR DATABASE URL HERE:
PRODUCTION_DB_URL = "postgresql://bucksport_db_user:AoNwTTxKMfRcNethp9tly3g24j3paHyD@dpg-d4o3lfeuk2gs7386r050-a/bucksport_db"

# If you can't find it in Render, try checking your Web Service environment variables:
# 1. Go to your Web Service (bucksport-api) in Render
# 2. Click "Environment" tab
# 3. Look for DATABASE_URL variable
# 4. Copy the value and paste it above

if not PRODUCTION_DB_URL:
    print("="*80)
    print("❌ ERROR: You need to set the DATABASE_URL")
    print("="*80)
    print("\nTo find your DATABASE_URL:")
    print("\nOption 1 - From Database:")
    print("  1. Go to https://dashboard.render.com")
    print("  2. Click on your PostgreSQL database")
    print("  3. Scroll to 'Connections' section")
    print("  4. Copy 'Internal Database URL'")
    print("\nOption 2 - From Web Service:")
    print("  1. Go to your Web Service (bucksport-api)")
    print("  2. Click 'Environment' tab")
    print("  3. Find DATABASE_URL variable")
    print("  4. Copy the value")
    print("\nThen paste it in this file at line 15 between the quotes")
    print("="*80)
    sys.exit(1)

# Set environment variable
os.environ["DATABASE_URL"] = PRODUCTION_DB_URL

print("\n" + "="*80)
print("STEP 1: Creating Donation table in production database...")
print("="*80)

# Run migration
import subprocess
result = subprocess.run([sys.executable, "bucksport_api/migrate_add_donations.py"], 
                       capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("❌ Migration failed:")
    print(result.stderr)
    sys.exit(1)

print("\n" + "="*80)
print("STEP 2: Importing sponsorship data from Excel...")
print("="*80)

# Run import
result = subprocess.run([sys.executable, "import_sponsorship_donations.py"], 
                       capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("❌ Import failed:")
    print(result.stderr)
    sys.exit(1)

print("\n" + "="*80)
print("✅ SUCCESS! Production database is ready.")
print("="*80)
print("\nNext steps:")
print("1. Upload fundraising.html to /board via FileZilla")
print("2. Upload sponsorships_redirect.html to /board via FileZilla (rename to sponsorships.html)")
print("3. Test at https://admin.bucksportll.org/fundraising.html")

"""
Setup script for production database - creates Donation table and imports data.
Run this ONCE to set up the production database with donation/sponsorship data.
"""
import os
import sys

# You need to set your production database URL
# Get this from Render dashboard -> Database -> Internal Database URL
PRODUCTION_DB_URL = input("Enter your production DATABASE_URL from Render: ").strip()

if not PRODUCTION_DB_URL:
    print("❌ Error: DATABASE_URL is required")
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

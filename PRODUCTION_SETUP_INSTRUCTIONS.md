# Production Database Setup Instructions

Since we can't connect to the database externally, we need to run the migration and import from Render's shell.

## Option 1: Use Render Shell (Recommended)

1. Go to https://dashboard.render.com
2. Click on your **Web Service** (bucksport-api)
3. Click **"Shell"** tab in the left sidebar
4. This will open a terminal connected to your production server

5. Run these commands in the shell:

```bash
# Create the Donation table
python -c "
from sqlmodel import SQLModel, create_engine
import os
from models import Donation
engine = create_engine(os.getenv('DATABASE_URL'))
SQLModel.metadata.create_all(engine)
print('✅ Donation table created')
"

# Import the sponsorship data
python import_sponsorship_donations.py
```

## Option 2: Upload via API (Alternative)

If the shell doesn't work, we can create a temporary API endpoint to trigger the import:

1. I'll create a special endpoint `/api/admin/import-donations`
2. You visit that URL once in your browser
3. It will import all the data
4. We remove the endpoint after

Let me know which option you prefer!

## After Database is Set Up

Once the database has the donation data:

1. Upload `local_site/fundraising.html` to `/board` via FileZilla
2. Upload `local_site/sponsorships_redirect.html` to `/board/sponsorships.html` via FileZilla
3. Test at https://admin.bucksportll.org/fundraising.html

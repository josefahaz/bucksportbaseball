# Bucksport Baseball/Softball Website - Requirements Documentation

## Overview
This document outlines all dependencies, requirements, and external services used in the Bucksport Little League website project.

---

## Backend Requirements (Python/FastAPI)

### Core Framework
- **FastAPI** `0.111.0` - Modern web framework for building APIs
- **Uvicorn** `0.29.0` - ASGI server with standard extras (websockets, httptools, uvloop)
- **SQLModel** `0.0.16` - SQL database ORM built on SQLAlchemy and Pydantic

### Database
- **psycopg** `3.2.3` - PostgreSQL adapter with binary and pool extras
  - Used for production PostgreSQL database on Render
  - Includes connection pooling for better performance
- **SQLite** - Built-in Python database (used for local development)

### Authentication & Security
- **python-jose[cryptography]** `3.3.0` - JWT token creation and validation
- **google-auth** `2.27.0` - Google OAuth authentication
- **google-auth-oauthlib** `1.2.0` - OAuth 2.0 client library
- **google-auth-httplib2** `0.2.0` - HTTP library for Google Auth

### Data Processing & Validation
- **Pydantic[email]** `2.11.7` - Data validation with email support
- **python-multipart** `0.0.7` - Form data parsing
- **python-dotenv** `1.0.0` - Environment variable management

### Utility Libraries
- **PyPDF2** `3.0.1` - PDF file processing (for order extraction)
- **openpyxl** `3.1.2` - Excel file reading/writing (for sponsorship data)

### Installation
```bash
cd bucksport_api
pip install -r requirements.txt
```

---

## Frontend Requirements

### CSS Framework
- **Tailwind CSS** - Loaded via CDN
  - URL: `https://cdn.tailwindcss.com`
  - Version: Latest (CDN auto-updates)
  - Usage: Utility-first CSS framework for styling

### Icons
- **Font Awesome** `6.4.0` - Icon library
  - URL: `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css`
  - Usage: Icons throughout the interface

### JavaScript
- **Vanilla JavaScript** - No framework dependencies
- Custom modules:
  - `js/mobile-detect.js` - Mobile device detection
  - `js/auth.js` - Authentication handling
  - `js/activity-log.js` - Activity logging system

### Browser Requirements
- Modern browsers with ES6+ support
- Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

---

## Production Environment (Render.com)

### Services Required
1. **Web Service** - FastAPI backend
   - Type: Web Service
   - Build Command: `pip install -r bucksport_api/requirements.txt`
   - Start Command: `cd bucksport_api && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Python Version: 3.13.4

2. **PostgreSQL Database**
   - Type: PostgreSQL
   - Plan: Free tier or higher
   - Auto-provisioned by Render

3. **Static Site** - Frontend (optional)
   - Type: Static Site
   - Build Command: None
   - Publish Directory: `local_site`

### Environment Variables Required
```bash
# Database (auto-set by Render)
DATABASE_URL=postgresql://...

# Environment
ENVIRONMENT=production

# Google OAuth (if using authentication)
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret

# JWT Secret
SECRET_KEY=your_secret_key_here
```

### Database Tables
The following tables are created automatically via SQLModel:
- `team` - Team information
- `player` - Player roster
- `event` - Events and games
- `inventoryitem` - Equipment inventory
- `boardmember` - Board member directory
- `coach` - Coach information
- `location` - Field/location data
- `scheduleevent` - Game schedule
- `user` - User accounts
- `activitylog` - Activity tracking (requires migration)

---

## Development Environment

### Local Setup
1. **Python Environment**
   ```bash
   cd bucksport_api
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment File** (`.env`)
   ```bash
   ENVIRONMENT=development
   DATABASE_URL=sqlite:///database.db
   SECRET_KEY=dev_secret_key
   ```

3. **Run Development Server**
   ```bash
   cd bucksport_api
   uvicorn main:app --reload --port 8000
   ```

4. **Frontend Development**
   - Open `local_site/index.html` in browser
   - Or use a local server: `python -m http.server 8080`

### Database Initialization
```bash
# Seed initial data
python seed_users.py
python seed_board_coaches.py
python seed_inventory.py

# Or for production
python seed_production_inventory.py
```

---

## API Endpoints

### Authentication
- `POST /auth/google` - Google OAuth login
- `POST /auth/logout` - User logout

### Teams & Players
- `GET /api/teams` - List all teams
- `POST /api/teams` - Create team
- `GET /api/players` - List players
- `POST /api/players` - Add player

### Inventory
- `GET /api/inventory` - List inventory items
- `POST /api/inventory` - Add item
- `PUT /api/inventory/{item_id}` - Update item
- `DELETE /api/inventory/{item_id}` - Delete item
- `GET /api/inventory/summary` - Inventory summary
- `GET /api/inventory/categories` - List categories
- `GET /api/inventory/statuses` - List statuses

### Activity Logs
- `GET /api/activity-logs` - Get activity logs (with optional page filter)
- `POST /api/activity-logs` - Create activity log entry

### Schedule
- `GET /api/schedule` - Get schedule events
- `POST /api/schedule` - Create schedule event

### Board & Coaches
- `GET /api/board-members` - List board members
- `GET /api/coaches` - List coaches

---

## File Structure

```
Softball_Baseball_Bucksport/
├── bucksport_api/              # Backend API
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Database models
│   ├── auth_models.py          # Auth models
│   ├── auth_routes.py          # Auth endpoints
│   ├── database.py             # Database configuration
│   ├── requirements.txt        # Python dependencies
│   ├── seed_*.py               # Database seeding scripts
│   └── migrate_*.py            # Migration scripts
│
├── local_site/                 # Frontend
│   ├── index.html              # Home page
│   ├── teams.html              # Teams page
│   ├── inventory.html          # Inventory management
│   ├── schedule.html           # Schedule page
│   ├── fundraising.html        # Fundraising page
│   ├── sponsorships.html       # Sponsorship transparency page
│   ├── sponsors_data.json      # Sponsor data
│   ├── js/                     # JavaScript modules
│   │   ├── auth.js
│   │   ├── activity-log.js
│   │   └── mobile-detect.js
│   └── mobile/                 # Mobile-optimized pages
│
├── *.xlsx                      # Excel data files
├── *.csv                       # CSV data files
└── *.md                        # Documentation
```

---

## Data Files

### Sponsorship Data
- **Source**: `Softball AND Baseball Banner & Sponsorship Log.xlsx`
- **Processed**: `sponsors_data.json` (68 sponsors with full history)
- **Scripts**:
  - `reorganize_sponsorship.py` - Creates master sheet
  - `export_all_sponsors_for_website.py` - Exports to JSON

### Inventory Data
- **Source**: `inventory_upload.csv` (125 items)
- **Scripts**:
  - `import_inventory_from_csv.py` - Import to database
  - `seed_production_inventory.py` - Production seeding

---

## Security Considerations

### Authentication
- JWT tokens for session management
- Google OAuth for user authentication
- Secure password hashing (if using local auth)

### Database
- Connection pooling to prevent exhaustion
- Prepared statements (SQLModel/SQLAlchemy)
- Environment-based configuration

### CORS
- Configured in `main.py`
- Allows frontend to communicate with backend
- Production URLs should be whitelisted

---

## Monitoring & Maintenance

### Activity Logging
- All inventory changes tracked
- User actions logged with timestamps
- Persistent database storage
- Accessible via Activity Log button

### Database Backups
- Render provides automatic PostgreSQL backups
- Excel/CSV files backed up with timestamps
- Local SQLite database for development

### Updates Required
1. Run database migrations when models change
2. Update `requirements.txt` when adding dependencies
3. Clear browser cache after frontend updates
4. Re-seed data if schema changes significantly

---

## Common Issues & Solutions

### Issue: Activity Log Not Working
**Solution**: Run migration script
```bash
python migrate_add_activity_log.py
```

### Issue: Missing Inventory Items
**Solution**: Re-seed production database
```bash
python seed_production_inventory.py
```

### Issue: CORS Errors
**Solution**: Check CORS configuration in `main.py` and verify API_BASE_URL in frontend

### Issue: Database Connection Errors
**Solution**: Verify DATABASE_URL environment variable and check Render database status

---

## Version Information

- **Python**: 3.13.4
- **FastAPI**: 0.111.0
- **PostgreSQL**: Latest (Render managed)
- **Last Updated**: January 11, 2026

---

## Support & Documentation

- **Deployment Guide**: `DEPLOY_PRODUCTION.md`
- **Production Fix Guide**: `PRODUCTION_FIX_GUIDE.md`
- **Auth Setup**: `AUTH_SETUP.md`
- **Environment Setup**: `ENV_SETUP_GUIDE.md`

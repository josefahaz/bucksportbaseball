# Authentication Setup Guide

## Overview
This guide will help you set up Google OAuth authentication for the Bucksport Little League website.

## Prerequisites
- Google Workspace account for bucksportll.org domain
- Access to Google Cloud Console

## Step 1: Set Up Google OAuth

### 1.1 Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Name it "Bucksport Little League"

### 1.2 Enable Google+ API
1. In the Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google+ API"
3. Click "Enable"

### 1.3 Create OAuth 2.0 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Web application"
4. Name it "Bucksport LL Website"
5. Add Authorized JavaScript origins:
   - `http://localhost:8000` (for local development)
   - `https://yourdomain.com` (your production domain)
6. Add Authorized redirect URIs:
   - `http://localhost:8000/login.html`
   - `https://yourdomain.com/login.html`
7. Click "Create"
8. **Copy the Client ID** - you'll need this!

### 1.4 Configure OAuth Consent Screen
1. Go to "APIs & Services" > "OAuth consent screen"
2. Choose "Internal" (for Google Workspace users only)
3. Fill in:
   - App name: "Bucksport Little League Portal"
   - User support email: your email
   - Developer contact: your email
4. Add scopes:
   - `.../auth/userinfo.email`
   - `.../auth/userinfo.profile`
5. Save and continue

## Step 2: Update Configuration Files

### 2.1 Update login.html
1. Open `local_site/login.html`
2. Find line with `data-client_id="YOUR_GOOGLE_CLIENT_ID"`
3. Replace `YOUR_GOOGLE_CLIENT_ID` with your actual Client ID from Step 1.3

### 2.2 Set Environment Variables
Create a `.env` file in the `bucksport_api` directory:

```bash
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
```

**Important:** Generate a secure JWT secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Step 3: Install Dependencies

```bash
cd bucksport_api
pip install -r requirements.txt
```

## Step 4: Initialize Database and Seed Users

```bash
# Run the user seeding script
python seed_users.py
```

This will create all 14 users from your list:
- 6 Admins (full access)
- 8 Board Members (read-only on Fundraising)

## Step 5: Start the Server

```bash
uvicorn main:app --reload --port 8000
```

## Step 6: Test Authentication

1. Open browser to `http://localhost:8000/login.html`
2. Click "Sign in with Google"
3. Choose your @bucksportll.org account
4. You should be redirected to the home page

## User Roles

### Admins (Full Access)
- Erick Kennard (ekennard@bucksportll.org)
- Jamie Bowden (jbowden@bucksportll.org) - President
- Joby Robinson (jrobinson@bucksportll.org) - Treasurer
- Joseph Hazlett (jhazlett@bucksportll.org)
- Katie Littlefield (klittlefield@bucksportll.org)
- Kim Burgess (kburgess@bucksportll.org)

### Board Members (Limited Access)
- Ashley Kennard (akennard@bucksportll.org)
- Christopher Rennick (crennick@bucksportll.org)
- Harold Littlefield (hlittlefield@bucksportll.org)
- Lisa Hazlett (lhazlett@bucksportll.org)
- Ryan Lightbody (rlightbody@bucksportll.org)
- Shelby Emery (semery@bucksportll.org)
- Taylor Beaulieu (tbeaulieu@bucksportll.org)
- Whitney Wentworth (wwentworth@bucksportll.org)

## Features

### Session Management
- Users stay logged in for 7 days
- Token automatically verified on each page load
- Logout button in header

### Access Control
- All pages require authentication
- Board members have read-only access to Fundraising page
- Admins can add new users via admin panel

### Activity Logging
- All actions logged with actual user name
- Detailed change tracking with before/after values

## Adding New Users

Admins can add new users:
1. Log in as an admin
2. Navigate to user management (to be implemented in UI)
3. Or use API directly:

```bash
curl -X POST http://localhost:8000/auth/users \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@bucksportll.org",
    "first_name": "John",
    "last_name": "Doe",
    "role": "board_member"
  }'
```

## Troubleshooting

### "Invalid Google token" error
- Verify Client ID is correct in login.html
- Check that OAuth consent screen is configured
- Ensure Google+ API is enabled

### "User not authorized" error
- User email must be in the database
- Run `python seed_users.py` to add initial users
- Admins can add new users via API

### Token expired
- Tokens last 7 days
- User will be automatically redirected to login
- Simply log in again

## Security Notes

1. **Never commit** `.env` file to git
2. **Change** the JWT_SECRET_KEY in production
3. **Use HTTPS** in production
4. **Restrict** OAuth to @bucksportll.org domain only
5. **Backup** the database regularly

## Production Deployment

When deploying to production:

1. Update `login.html` with production Client ID
2. Add production domain to Google OAuth settings
3. Set environment variables on server
4. Use HTTPS (required for Google OAuth)
5. Update CORS settings in `main.py` if needed

## Support

For issues or questions:
- Contact: Joe Hazlett (jhazlett@bucksportll.org)
- Check logs in terminal for error messages
- Verify all environment variables are set correctly

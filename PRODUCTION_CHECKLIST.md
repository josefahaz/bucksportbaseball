# Production Deployment Checklist

## ✅ Git Status
**Status:** All changes committed and pushed to GitHub
- Latest commit: `8bde9c7` - Map dev login emails to proper first and last names
- Branch: `main`
- Remote: Up to date with `origin/main`

---

## 🔐 OAuth Configuration Status

### Current Configuration
**Client ID in login.html:**
```
YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com
```

**Environment Variables (.env):**
```
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
JWT_SECRET_KEY=your-secure-jwt-secret-key-here
```

**Note:** The actual credentials are configured in:
- `local_site/login.html` (line 41)
- `bucksport_api/.env` (not committed to git)

### ⚠️ IMPORTANT: Production Setup Required

**For production deployment, you MUST:**

1. **Verify Google Cloud Project Settings:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Ensure the OAuth client is configured for your production domain
   - Add authorized JavaScript origins:
     - Your production domain (e.g., `https://bucksportll.org`)
   - Add authorized redirect URIs:
     - `https://yourdomain.com/login.html`

2. **Update OAuth Consent Screen:**
   - Set to "Internal" for Google Workspace users only
   - This restricts login to @bucksportll.org emails only

3. **Generate New JWT Secret for Production:**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   - Replace the JWT_SECRET_KEY in production .env
   - **NEVER** use the same secret in dev and production

4. **Verify Domain Restriction:**
   - Backend enforces @bucksportll.org domain
   - File: `bucksport_api/auth.py` - `verify_google_token()` function

---

## 📋 Pre-Deployment Checklist

### Backend Setup
- [ ] Create production `.env` file with:
  - [ ] Production Google Client ID
  - [ ] Secure JWT secret key (different from dev)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Initialize database
- [ ] Run user seeding script: `python seed_users.py`
- [ ] Test backend API endpoints

### Frontend Setup
- [ ] Update `login.html` with production Client ID (if different)
- [ ] Verify all HTML files are included
- [ ] Test all navigation links
- [ ] Verify auth.js is loaded on all pages

### Google OAuth Setup
- [ ] OAuth client created in Google Cloud Console
- [ ] Authorized JavaScript origins configured
- [ ] Authorized redirect URIs configured
- [ ] OAuth consent screen set to "Internal"
- [ ] Required scopes added:
  - [ ] userinfo.email
  - [ ] userinfo.profile

### Database
- [ ] Users table created
- [ ] All 14 users seeded:
  - [ ] 6 Admins
  - [ ] 8 Board Members
- [ ] Test user login for each role

### Security
- [ ] JWT secret is secure and unique
- [ ] Domain restriction enforced (@bucksportll.org)
- [ ] HTTPS enabled in production
- [ ] CORS configured for production domain
- [ ] .env file NOT committed to git (in .gitignore)

### Testing
- [ ] Test Google OAuth login
- [ ] Test admin access (all pages)
- [ ] Test board member access (read-only on Fundraising)
- [ ] Test logout functionality
- [ ] Test session persistence (7 days)
- [ ] Test unauthorized access redirect

---

## 🚀 Deployment Steps

### 1. Deploy Backend
```bash
cd bucksport_api
# Set up production environment
# Install dependencies
pip install -r requirements.txt
# Run database initialization
python seed_users.py
# Start production server (use gunicorn or similar)
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. Deploy Frontend
- Upload all files from `local_site/` to your web server
- Ensure proper file permissions
- Configure web server to serve static files

### 3. Configure Web Server
- Set up HTTPS/SSL certificate
- Configure reverse proxy if needed
- Set proper CORS headers
- Enable gzip compression

### 4. Post-Deployment Verification
- [ ] Visit production login page
- [ ] Test Google OAuth login
- [ ] Verify user roles and permissions
- [ ] Test all pages and features
- [ ] Check activity logging
- [ ] Verify logout functionality

---

## 🔧 Current Features

### Authentication
- ✅ Google OAuth 2.0 integration
- ✅ Domain restriction (@bucksportll.org)
- ✅ JWT token-based sessions (7 days)
- ✅ Development mode for local testing
- ✅ Automatic redirect for unauthenticated users

### User Management
- ✅ 6 Admins with full access
- ✅ 8 Board Members with read-only on Fundraising
- ✅ User info displayed in sidebar
- ✅ Logout button in sidebar

### Pages
- ✅ Home
- ✅ Teams
- ✅ Coach Dashboard
- ✅ Equipment Inventory
- ✅ Schedule
- ✅ Concessions
- ✅ Event Concessions
- ✅ Fundraising & Donations (read-only for board members)

### UI Features
- ✅ Welcome message with first name in sidebar
- ✅ Logout button in sidebar
- ✅ Activity logging with user names
- ✅ Role-based UI adjustments
- ✅ Read-only mode for Fundraising (board members)

---

## 📞 Support

If you encounter issues during deployment:
1. Check AUTH_SETUP.md for detailed OAuth setup
2. Verify .env file configuration
3. Check browser console for errors
4. Verify backend logs for authentication errors
5. Ensure Google Cloud OAuth settings match your domain

---

## 🔒 Security Notes

**CRITICAL:**
- Never commit `.env` file to git
- Use different JWT secrets for dev and production
- Ensure OAuth consent screen is set to "Internal"
- Verify HTTPS is enabled in production
- Regularly rotate JWT secret keys
- Monitor authentication logs for suspicious activity

---

## 📝 Next Steps

1. **Immediate:** Verify Google Cloud OAuth settings for production domain
2. **Before Deploy:** Generate new JWT secret for production
3. **After Deploy:** Test all authentication flows
4. **Ongoing:** Monitor user access and activity logs

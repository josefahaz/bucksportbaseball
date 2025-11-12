# Production Deployment Guide

## 🎯 Goal
Deploy full production site with Google OAuth and shared database.

---

## Step 1: Deploy Backend API to Render

### 1.1 Create Render Account
1. Go to [https://render.com](https://render.com)
2. Sign up with GitHub (easiest)

### 1.2 Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `josefahaz/bucksportbaseball`
3. Click **"Connect"**

### 1.3 Configure Service
Fill in these settings:

**Basic Settings:**
- **Name:** `bucksport-api`
- **Region:** US East (Ohio) or closest to you
- **Branch:** `main`
- **Root Directory:** `bucksport_api`
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Instance Type:**
- Select **"Free"** (for now, can upgrade later)

### 1.4 Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**

Add these three variables:

```
ENVIRONMENT=production
```

```
GOOGLE_CLIENT_ID=880101265433-3ef04k59hfr794hmqptf6iro7758v8ug.apps.googleusercontent.com
```

```
JWT_SECRET_KEY=VDS7iYJMxq9BRb7Jj4uxb3264hWnCyTq7KLWmCmewmk
```

### 1.5 Deploy
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. You'll get a URL like: `https://bucksport-api.onrender.com`
4. **SAVE THIS URL** - you'll need it!

### 1.6 Initialize Database
Once deployed, go to the **"Shell"** tab in Render and run:
```bash
python seed_users.py
```

This creates all 14 users in the production database.

---

## Step 2: Update Frontend Configuration

### 2.1 Update API URL
Update `local_site/js/api.js` line 4 with your Render API URL:

**Before:**
```javascript
: '/api';  // Production (proxied through same domain)
```

**After:**
```javascript
: 'https://bucksport-api.onrender.com';  // Your actual Render URL
```

### 2.2 Enable OAuth (Disable Dev Mode)
Update `local_site/login.html` line 272:

**Before:**
```javascript
const USE_DEV_MODE = true;
```

**After:**
```javascript
const USE_DEV_MODE = false;
```

---

## Step 3: Configure Google OAuth for Production

### 3.1 Update Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to: **APIs & Services** > **Credentials**
3. Find your OAuth 2.0 Client ID: `880101265433-3ef04k59hfr794hmqptf6iro7758v8ug`
4. Click **Edit**

### 3.2 Add Authorized Origins
Under **"Authorized JavaScript origins"**, add:
```
https://bucksportbaseball.onrender.com
```

### 3.3 Add Authorized Redirect URIs
Under **"Authorized redirect URIs"**, add:
```
https://bucksportbaseball.onrender.com/login.html
```

### 3.4 Save
Click **"Save"** and wait 5-10 minutes for changes to propagate.

---

## Step 4: Deploy Frontend to Production

### 4.1 Commit Changes
```bash
git add local_site/js/api.js local_site/login.html
git commit -m "Configure for production deployment with OAuth"
git push
```

### 4.2 Deploy to Render/Netlify
Your frontend should auto-deploy when you push to GitHub.

---

## Step 5: Test Production

### 5.1 Visit Production Site
Go to: `https://bucksportbaseball.onrender.com/login.html`

### 5.2 Test Google OAuth
1. Click **"Sign in with Google"** button
2. Select your @bucksportll.org account
3. Should redirect to homepage
4. Should see "Welcome, [FirstName]" in sidebar

### 5.3 Test Data Sharing
1. Login as one user
2. Add a concessions item
3. Logout
4. Login as different user
5. Should see the same item ✅

### 5.4 Test Permissions
**Admin User (jhazlett@bucksportll.org):**
- Can edit all pages
- Can add/edit/delete items

**Board Member (akennard@bucksportll.org):**
- Can view all pages
- Fundraising page is read-only
- Can edit other pages

---

## 🔧 Troubleshooting

### Google Button Not Showing
- Wait 10 minutes after updating Google Cloud Console
- Clear browser cache (Ctrl+Shift+R)
- Check browser console for errors

### API Not Connecting
- Verify Render service is running (green status)
- Check API URL in `api.js` matches Render URL
- Check CORS is enabled in backend

### Users Can't Login
- Verify user exists in database (run seed_users.py)
- Check email is @bucksportll.org
- Verify OAuth consent screen is set to "Internal"

---

## 📊 Production URLs

**Frontend:** https://bucksportbaseball.onrender.com  
**Backend API:** https://bucksport-api.onrender.com  
**API Docs:** https://bucksport-api.onrender.com/docs  

---

## ✅ Success Checklist

- [ ] Backend deployed to Render
- [ ] Database seeded with users
- [ ] Frontend API URL updated
- [ ] Dev mode disabled
- [ ] Google OAuth configured for production domain
- [ ] Frontend deployed
- [ ] Google Sign-In button appears
- [ ] Can login with @bucksportll.org account
- [ ] Data persists between users
- [ ] Permissions work correctly

---

## 🎉 You're Live!

Once all steps are complete, your production site will be fully functional with:
- ✅ Google OAuth authentication
- ✅ Shared database
- ✅ Role-based permissions
- ✅ Real-time data sync
- ✅ Secure JWT tokens

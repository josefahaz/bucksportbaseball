# Environment Configuration Guide

## Overview
This guide explains how to manage separate environment configurations for development and production.

---

## 📁 File Structure

```
bucksport_api/
├── .env                    # Development environment (local)
├── .env.production         # Production environment (server)
└── .env.example           # Template (safe to commit)
```

---

## 🔧 Setup Instructions

### 1. Generate Secure JWT Secrets

**For Development:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**For Production (generate a different one):**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. Create Development .env File

Create `bucksport_api/.env`:
```bash
# Development Environment
GOOGLE_CLIENT_ID=880101265433-3ef04k59hfr794hmqptf6iro7758v8ug.apps.googleusercontent.com
JWT_SECRET_KEY=your-dev-secret-key-here
```

### 3. Create Production .env File

Create `bucksport_api/.env.production`:
```bash
# Production Environment
GOOGLE_CLIENT_ID=880101265433-3ef04k59hfr794hmqptf6iro7758v8ug.apps.googleusercontent.com
JWT_SECRET_KEY=your-production-secret-key-here
```

**⚠️ IMPORTANT:** Use a **different** JWT secret for production!

### 4. Create .env.example (Template)

Create `bucksport_api/.env.example` (safe to commit):
```bash
# Environment Configuration Template
# Copy this file to .env for development or .env.production for production
# DO NOT commit actual .env files to git

GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
JWT_SECRET_KEY=your-secure-jwt-secret-key
```

---

## 🚀 Running the Application

### Development Mode (Default)
```bash
cd bucksport_api
uvicorn main:app --reload --port 8000
```
This automatically loads `.env`

### Production Mode
```bash
cd bucksport_api
ENVIRONMENT=production uvicorn main:app --host 0.0.0.0 --port 8000
```
This loads `.env.production`

**Or set environment variable first:**
```bash
# Windows PowerShell
$env:ENVIRONMENT="production"
uvicorn main:app --host 0.0.0.0 --port 8000

# Windows CMD
set ENVIRONMENT=production
uvicorn main:app --host 0.0.0.0 --port 8000

# Linux/Mac
export ENVIRONMENT=production
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Generate different JWT secrets for dev and production
- Keep `.env` files out of git (already in .gitignore)
- Use strong, random secrets (32+ characters)
- Rotate production secrets regularly
- Use environment variables on production servers
- Keep `.env.example` updated as a template

### ❌ DON'T:
- Commit `.env` or `.env.production` to git
- Share production secrets in chat/email
- Use the same secret in dev and production
- Hard-code secrets in source code
- Use weak or predictable secrets

---

## 📋 Deployment Checklist

### Before Deploying to Production:

- [ ] Generate new JWT secret for production
- [ ] Create `.env.production` on production server
- [ ] Verify Google OAuth Client ID is correct
- [ ] Set `ENVIRONMENT=production` on server
- [ ] Test that production env loads correctly
- [ ] Verify secrets are different from dev
- [ ] Confirm `.env` files are in .gitignore
- [ ] Document where production secrets are stored

---

## 🔍 Verification

### Check Which Environment is Loaded

When you start the server, you'll see:
```
INFO:     Running in development mode
```
or
```
INFO:     Running in production mode
```

### Test Environment Variables

Create a test endpoint (remove after testing):
```python
@app.get("/test-env")
def test_env():
    return {
        "environment": os.getenv('ENVIRONMENT', 'development'),
        "jwt_secret_set": bool(os.getenv('JWT_SECRET_KEY')),
        "client_id_set": bool(os.getenv('GOOGLE_CLIENT_ID'))
    }
```

---

## 🐳 Docker Deployment (Optional)

If using Docker, pass environment variables:

```dockerfile
# Dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Run with production env
docker run -e ENVIRONMENT=production \
  -e GOOGLE_CLIENT_ID=your-id \
  -e JWT_SECRET_KEY=your-secret \
  -p 8000:8000 your-image
```

---

## 🆘 Troubleshooting

### Environment Not Loading
**Problem:** Server uses wrong environment  
**Solution:** Explicitly set `ENVIRONMENT` variable before starting

### Secrets Not Found
**Problem:** `KeyError` or authentication fails  
**Solution:** Verify `.env` file exists and has correct format

### Wrong Environment in Production
**Problem:** Dev secrets used in production  
**Solution:** Check `ENVIRONMENT` variable is set to `production`

### Git Committed .env File
**Problem:** Secrets exposed in git  
**Solution:** 
1. Remove from git: `git rm --cached bucksport_api/.env`
2. Add to .gitignore (already done)
3. Rotate all secrets immediately
4. Force push: `git push --force`

---

## 📞 Quick Reference

| Action | Command |
|--------|---------|
| Generate secret | `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| Run dev | `uvicorn main:app --reload` |
| Run production | `ENVIRONMENT=production uvicorn main:app` |
| Check env | Look for "Running in X mode" in logs |

---

## 🔄 Rotating Secrets

### When to Rotate:
- Every 90 days (recommended)
- After team member leaves
- If secret is compromised
- Before major deployment

### How to Rotate:
1. Generate new secret
2. Update `.env.production` on server
3. Restart application
4. All users will need to re-login (tokens invalidated)
5. Update backup/documentation

---

## ✅ Current Status

**Development (.env):**
- ✅ File exists
- ✅ In .gitignore
- ✅ JWT secret configured

**Production (.env.production):**
- ⚠️ Needs to be created on production server
- ⚠️ Needs different JWT secret from dev
- ⚠️ Set ENVIRONMENT=production when running

**Code:**
- ✅ Environment detection implemented
- ✅ Automatic .env file loading
- ✅ Logging shows which environment is active

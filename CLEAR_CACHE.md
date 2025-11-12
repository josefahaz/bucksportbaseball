# Browser Cache Issue - How to Fix

## The Problem
You're seeing old navigation links (Fundraising & Marketing) because your browser has cached the old HTML files.

## Verified Clean
All HTML files have been verified and are clean - no fundraising or marketing links exist in the code.

## Solutions (Try in order)

### 1. Hard Refresh (Quickest)
**Windows/Linux:**
- Press `Ctrl + Shift + R` or `Ctrl + F5`

**Mac:**
- Press `Cmd + Shift + R`

### 2. Clear Browser Cache
**Chrome/Edge:**
1. Press `Ctrl + Shift + Delete` (or `Cmd + Shift + Delete` on Mac)
2. Select "Cached images and files"
3. Choose "All time"
4. Click "Clear data"

**Firefox:**
1. Press `Ctrl + Shift + Delete`
2. Select "Cache"
3. Choose "Everything"
4. Click "Clear Now"

### 3. Open in Incognito/Private Window
**Chrome/Edge:**
- Press `Ctrl + Shift + N`

**Firefox:**
- Press `Ctrl + Shift + P`

Then navigate to `http://localhost:8000`

### 4. Restart the Server (If above doesn't work)
1. Stop the server (Ctrl+C in terminal)
2. Start it again:
   ```bash
   cd bucksport_api
   uvicorn main:app --reload --port 8000
   ```
3. Hard refresh the browser

### 5. Nuclear Option - Clear Everything
1. Close all browser windows
2. Clear all browser data (history, cache, cookies)
3. Restart browser
4. Navigate to `http://localhost:8000/login.html`

## What You Should See

After clearing cache, the navigation should show:
- ✅ Home
- ✅ Teams
- ✅ Coach Dashboard
- ✅ Equipment Inventory
- ✅ Schedule
- ✅ Concessions
- ✅ Event Concessions

**NOT showing:**
- ❌ Fundraising & Donations
- ❌ Marketing

## Still Having Issues?

If you still see the old links after trying all the above:
1. Check the browser's Developer Tools (F12)
2. Go to Network tab
3. Reload the page
4. Look for the HTML file being loaded
5. Check if it says "from cache" or "200 OK"
6. If it says "from cache", the hard refresh didn't work - try incognito mode

## Prevention

To avoid this in the future during development:
1. Keep Developer Tools open (F12)
2. Check "Disable cache" in the Network tab
3. This prevents caching while DevTools is open

# Local Test Site

Static HTML page to test the FastAPI backend while developing locally.

## Usage
1. Ensure FastAPI is running locally (`uvicorn main:app --reload`).
2. Open `index.html` in your browser (double-click).
3. Fill out the form and click Submit – you should see “Success!” and the player record appear at `http://127.0.0.1:8000/docs#/players/read_players_players__get`.

When you’re ready to push the form to bucksportll.org, copy `embed.js` (update URL) and matching markup there.

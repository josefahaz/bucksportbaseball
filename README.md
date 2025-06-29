# Bucksport Baseball/Softball API

FastAPI backend providing registration, schedule, and roster endpoints for the Wix front-end site.

## Local development
```bash
# (optional) create virtualenv
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload
```

API will be served at `http://127.0.0.1:8000` with interactive docs at `/docs`.

## Deploying
Free hosts such as Render.com or Fly.io can build a FastAPI service from this repo automatically. Ensure `uvicorn main:app --host 0.0.0.0 --port $PORT` is the start command.

## Connecting from Wix (Velo)
In Velo’s JavaScript:
```js
import {fetch} from 'wix-fetch';

export function regForm_submit(event) {
  const data = {
    first_name: $w('#first').value,
    last_name: $w('#last').value,
    birthdate: $w('#dob').value,
    email: $w('#email').value,
    phone: $w('#phone').value,
    team_id: $w('#teamDropdown').value
  };

  fetch('https://YOUR-API-URL.onrender.com/players', {
    method: 'post',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  .then(res => res.json())
  .then(() => { wixWindow.openLightbox('Thanks'); })
  .catch(err => console.error(err));
}
```
Update CORS origins in `main.py` with your actual Wix domain before deploying.

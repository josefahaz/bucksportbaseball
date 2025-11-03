// Embed script for bucksportll.org to submit player registration
async function submitRegistration() {
  const data = {
    first_name: document.querySelector('#first').value,
    last_name:  document.querySelector('#last').value,
    birthdate:  document.querySelector('#dob').value,
    email:      document.querySelector('#email').value,
    phone:      document.querySelector('#phone').value,
    team_id:    document.querySelector('#team').value
  };

  try {
    const res = await fetch('https://YOUR-RENDER-URL/players', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error(await res.text());
    alert('Registration received!');
  } catch(err) {
    alert('Error: ' + err.message);
  }
}

// attach to a button with id="reg-submit"
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.querySelector('#reg-submit');
  if (btn) btn.addEventListener('click', submitRegistration);
});

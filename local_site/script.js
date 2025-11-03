document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');
  const submitBtn = document.getElementById('reg-submit');
  const status = document.getElementById('status');
  const apiBase = 'http://127.0.0.1:8000/api'; // local FastAPI with /api prefix

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Show loading state
    const originalBtnText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.innerHTML = `
      <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-purple-700 inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      Processing...`;
    
    status.textContent = '';
    status.className = 'text-center mt-4 text-sm';
    
    const formData = {
      first_name: document.getElementById('first').value.trim(),
      last_name: document.getElementById('last').value.trim(),
      birthdate: document.getElementById('dob').value,
      email: document.getElementById('email').value.trim(),
      phone: document.getElementById('phone').value.trim(),
      team_id: document.getElementById('team').value.trim() || null
    };

    try {
      const response = await fetch(`${apiBase}/players`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      const responseData = await response.json();
      
      if (!response.ok) {
        throw new Error(responseData.detail || 'Registration failed. Please try again.');
      }
      
      // Show success message
      status.textContent = '✅ Registration successful! Thank you!';
      status.className = 'text-center mt-4 text-sm text-green-600 font-medium';
      
      // Reset form
      form.reset();
      
      // Scroll to status message
      status.scrollIntoView({ behavior: 'smooth' });
      
      // Clear success message after 5 seconds
      setTimeout(() => {
        status.textContent = '';
      }, 5000);
      
    } catch (error) {
      console.error('Registration failed:', error);
      status.textContent = `❌ ${error.message || 'An error occurred. Please try again.'}`;
      status.className = 'text-center mt-4 text-sm text-red-600 font-medium';
    } finally {
      // Reset button state
      submitBtn.disabled = false;
      submitBtn.textContent = originalBtnText;
    }
  });
});

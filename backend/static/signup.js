const form = document.getElementById('signup-form');
const msg  = document.getElementById('message');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  // grab the data out of the form
  const formData = new FormData(form);

  try {
    const res = await fetch('http://192.168.68.62:8000/signup', {
      method:      'POST',
      credentials: 'include',    // if you ever want cookies/auth
      body:        formData      // automatically sets Content-Type: multipart/form-data
    });

    const data = await res.json();

    if (res.ok) {
      msg.textContent = `✅ Welcome, ${data.username}!`;
    } else {
      // FastAPI will usually send back { detail: "..." } on error
      msg.textContent = `❌ ${data.detail || data.error || res.statusText}`;
    }

  } catch (err) {
    msg.textContent = `⚠️ Network error: ${err.message}`;
  }
});
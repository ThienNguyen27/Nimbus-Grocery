// const form = document.getElementById('signup-form') as HTMLFormElement;
// const msg = document.getElementById('message') as HTMLParagraphElement;

// form.addEventListener('submit', async (e) => {
//   e.preventDefault();

//   const name = (document.getElementById('name') as HTMLInputElement).value;
//   const email = (document.getElementById('email') as HTMLInputElement).value;
//   const password = (document.getElementById('password') as HTMLInputElement).value;

//   const res = await fetch('/api/signup', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ name, email, password })
//   });

//   const data = await res.json();
//   msg.textContent = res.ok ? '✅ Sign-up successful!' : `❌ ${data.error}`;
// });

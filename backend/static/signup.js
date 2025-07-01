document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signup-form");
    const message = document.getElementById("message");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const name = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const data = { name, email, password };

        try {
            const response = await fetch("http://127.0.0.1:8000/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (response.ok) {
                message.textContent = "Signup successful!";
                message.className = "success";
            } else {
                console.error(result);
                message.textContent = result.detail || "Signup failed.";
                message.className = "error";
            }
        } catch (error) {
            console.error(error);
            message.textContent = "An error occurred.";
            message.className = "error";
        }
    });
});

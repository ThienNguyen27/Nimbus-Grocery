document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signup-form");
    const message = document.getElementById("message");
    const canvas = document.getElementById("preview");
    const video = document.getElementById("camera");
    const snapBtn = document.getElementById("snap");

    // Start webcam stream
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            console.error("Could not access camera:", err);
            alert("Could not access camera.");
        });

    // Take photo
    snapBtn.addEventListener("click", () => {
        const context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        canvas.style.display = "block";
    });

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const name = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        // Capture canvas as blob
        const blob = await new Promise(resolve => canvas.toBlob(resolve, "image/jpeg"));

        const formData = new FormData();
        formData.append("name", name);
        formData.append("email", email);
        formData.append("password", password);
        formData.append("photo", blob, "snapshot.jpg");

        try {
            const response = await fetch("http://127.0.0.1:8000/signup", {
                method: "POST",
                // headers: {
                //     "Content-Type": "application/json",
                // },
                body: formData,  // browser automatically sets Content-Type with boundaries
            });

            const result = await response.json();

            if (response.ok) {
                message.textContent = "Signup successful!";
                message.className = "success";

                // Redirect user to /signedin/page
                setTimeout(() => {
                    window.location.href = "http://localhost:3001/signin"; // or "/signedin/page.tsx" depending on your routing
                }, 1000);
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

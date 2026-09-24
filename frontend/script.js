async function generatePlan() {

    const text = document.getElementById("eventText").value.trim();

    const errorMessage =
        document.getElementById("errorMessage");

    errorMessage.innerText = "";

    if (text === "") {

        errorMessage.innerText =
            "Please enter an event description.";

        return;
    }

    try {

        const response = await fetch(
            "http://localhost:3000/generate",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    text: text
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {

            errorMessage.innerText =
                data.error || "Something went wrong.";

            return;
        }

        // Save result for result page
        localStorage.setItem(
            "eventPlan",
            JSON.stringify(data)
        );

        // Open result page
        window.location.href = "result.html";

    } catch (error) {

        console.error(error);

        errorMessage.innerText =
            "Cannot connect to backend. Please start the server.";
    }
}
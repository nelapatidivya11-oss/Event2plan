const API_URL = "/generate";

/* =========================
   GET SAVED EVENT DATA
========================= */

function getData() {
    try {
        return JSON.parse(localStorage.getItem("eventPlan"));
    } catch (error) {
        return null;
    }
}


/* =========================
   MONEY FORMAT
========================= */

function money(value) {

    if (typeof value === "number") {
        return "₹" + value.toLocaleString("en-IN");
    }

    if (value === null || value === undefined || value === "") {
        return "Not specified";
    }

    return value;
}


/* =========================
   CREATE TAG
========================= */

function createTag(text) {

    const div = document.createElement("div");

    div.className = "tag";

    div.textContent = text;

    return div;
}


/* =========================
   CREATE LIST ITEM
========================= */

function createListItem(text) {

    const div = document.createElement("div");

    div.className = "list-item";

    div.textContent = "✓ " + text;

    return div;
}


/* =========================
   GENERATE EVENT PLAN
========================= */

async function generatePlan() {

    const eventTextElement =
        document.getElementById("eventText");

    if (!eventTextElement) {
        console.error("eventText element not found");
        return;
    }

    const text = eventTextElement.value.trim();

    if (!text) {

        alert("Please describe your event first.");

        return;
    }

    const button =
        document.getElementById("generateBtn");

    if (button) {
        button.disabled = true;
        button.textContent = "Generating...";
    }

    try {

        console.log("Sending request to:", API_URL);

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text
            })

        });

        console.log("Response status:", response.status);

        const data = await response.json();

        console.log("Server response:", data);

        if (!response.ok) {

            throw new Error(
                data.error || "Failed to generate event plan."
            );

        }

        /* Save result */

        localStorage.setItem(
            "eventPlan",
            JSON.stringify(data)
        );

        /* Open result page */

        window.location.href = "result.html";

    } catch (error) {

        console.error("Generate error:", error);

        alert(
            "Unable to generate event plan.\n\n" +
            error.message
        );

    } finally {

        if (button) {

            button.disabled = false;

            button.textContent =
                "Generate Complete Plan";

        }

    }
}


/* =========================
   SHOW RESULT
========================= */

function showResult(data) {

    if (!data) {

        const errorBox =
            document.getElementById("errorBox");

        if (errorBox) {

            errorBox.textContent =
                "No event data found. Please create an event first.";

        }

        return;
    }


    if (data.error) {

        const errorBox =
            document.getElementById("errorBox");

        if (errorBox) {

            errorBox.textContent =
                data.error;

        }

        return;
    }


    /* Event Type */

    const eventType =
        document.getElementById("eventType");

    if (eventType) {

        eventType.textContent =
            data.event_type || "Not specified";

    }


    /* People */

    const people =
        document.getElementById("people");

    if (people) {

        people.textContent =
            data.people || "Not specified";

    }


    /* Location */

    const location =
        document.getElementById("location");

    if (location) {

        location.textContent =
            data.location || "Not specified";

    }


    /* Budget */

    const budget =
        document.getElementById("budget");

    if (budget) {

        budget.textContent =
            money(data.budget);

    }


    /* Requirements */

    const requirements =
        document.getElementById("requirements");

    if (requirements) {

        requirements.innerHTML = "";

        (data.requirements || []).forEach(item => {

            requirements.appendChild(
                createTag(item)
            );

        });

    }


    /* Budget Plan */

    const budgetPlan =
        document.getElementById("budgetPlan");

    if (budgetPlan) {

        budgetPlan.innerHTML = "";

        if (data.budget_plan) {

            Object.entries(data.budget_plan).forEach(
                ([key, value]) => {

                    const div =
                        document.createElement("div");

                    div.className =
                        "budget-item";

                    div.innerHTML = `
                        <span>${key}</span>
                        <strong>${money(value)}</strong>
                    `;

                    budgetPlan.appendChild(div);

                }
            );

        }

    }


    /* Menu */

    const menu =
        document.getElementById("menu");

    if (menu) {

        menu.innerHTML = "";

        (data.menu || []).forEach(item => {

            menu.appendChild(
                createListItem(item)
            );

        });

    }


    /* Music */

    const music =
        document.getElementById("music");

    if (music) {

        music.innerHTML = "";

        (data.music_suggestions || []).forEach(item => {

            music.appendChild(
                createListItem(item)
            );

        });

    }


    /* Checklist */

    const checklist =
        document.getElementById("checklist");

    if (checklist) {

        checklist.innerHTML = "";

        (data.checklist || []).forEach(
            (item, index) => {

                const div =
                    document.createElement("div");

                div.className =
                    "check-item";

                div.innerHTML = `
                    <span class="number">
                        ${index + 1}
                    </span>

                    <span>
                        ${item}
                    </span>
                `;

                checklist.appendChild(div);

            }
        );

    }


    /* Timeline */

    const timeline =
        document.getElementById("timeline");

    if (timeline) {

        timeline.innerHTML = "";

        (data.timeline || []).forEach(item => {

            const div =
                document.createElement("div");

            div.className =
                "timeline-item";

            div.innerHTML = `
                <strong>${item.time}</strong>
                <span>${item.activity}</span>
            `;

            timeline.appendChild(div);

        });

    }


    /* Summary */

    const summary =
        document.getElementById("summary");

    if (summary) {

        summary.textContent =
            data.summary ||
            "Your event plan has been generated successfully.";

    }

}


/* =========================
   PAGE LOAD
========================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        /* Result page */

        if (
            document.getElementById("eventType") ||
            document.getElementById("people")
        ) {

            const data = getData();

            showResult(data);

        }

    }
);

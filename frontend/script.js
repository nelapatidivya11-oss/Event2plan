const API_URL = "/generate";

// ===============================
// CREATE EVENT PAGE
// ===============================

async function generatePlan() {

    const eventText = document.getElementById("eventText");
    const button = document.getElementById("generateBtn");

    if (!eventText) {
        return;
    }

    const text = eventText.value.trim();

    if (!text) {
        alert("Please enter your event description.");
        return;
    }

    if (button) {
        button.disabled = true;
        button.textContent = "Understanding your event...";
    }

    try {

        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to generate event plan.");
        }

        // Save NLP result
        localStorage.setItem(
            "eventPlan",
            JSON.stringify(data)
        );

        // Go to result page
        window.location.href = "result.html";

    } catch (error) {

        console.error("Error:", error);

        alert(
            "Unable to generate event plan.\n\n" +
            error.message
        );

        if (button) {
            button.disabled = false;
            button.textContent = "✨ Generate Complete Plan";
        }
    }
}


// ===============================
// GET SAVED DATA
// ===============================

function getData() {

    try {

        const data = localStorage.getItem("eventPlan");

        if (!data) {
            return null;
        }

        return JSON.parse(data);

    } catch (error) {

        console.error("LocalStorage error:", error);
        return null;
    }
}


// ===============================
// MONEY FORMAT
// ===============================

function money(value) {

    if (
        typeof value === "number" &&
        !isNaN(value)
    ) {
        return "₹" + value.toLocaleString("en-IN");
    }

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return "Not specified";
    }

    return value;
}


// ===============================
// CREATE TAG
// ===============================

function createTag(text) {

    const div = document.createElement("div");

    div.className = "tag";

    div.textContent = text;

    return div;
}


// ===============================
// CREATE LIST ITEM
// ===============================

function createListItem(text) {

    const div = document.createElement("div");

    div.className = "list-item";

    div.textContent = "✓ " + text;

    return div;
}


// ===============================
// SHOW RESULT
// ===============================

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


    // ===============================
    // ERROR
    // ===============================

    if (data.error) {

        const errorBox =
            document.getElementById("errorBox");

        if (errorBox) {
            errorBox.textContent = data.error;
        }

        return;
    }


    // ===============================
    // EVENT TYPE
    // ===============================

    const eventType =
        document.getElementById("eventType");

    if (eventType) {

        eventType.textContent =
            data.event_type || "Not specified";
    }


    // ===============================
    // PEOPLE
    // ===============================

    const people =
        document.getElementById("people");

    if (people) {

        people.textContent =
            data.people || "Not specified";
    }


    // ===============================
    // LOCATION
    // ===============================

    const location =
        document.getElementById("location");

    if (location) {

        location.textContent =
            data.location || "Not specified";
    }


    // ===============================
    // BUDGET
    // ===============================

    const budget =
        document.getElementById("budget");

    if (budget) {

        budget.textContent =
            money(data.budget);
    }


    // ===============================
    // REQUIREMENTS
    // ===============================

    const requirements =
        document.getElementById("requirements");

    if (requirements) {

        requirements.innerHTML = "";

        const items =
            Array.isArray(data.requirements)
                ? data.requirements
                : [];

        items.forEach(item => {

            requirements.appendChild(
                createTag(item)
            );
        });
    }


    // ===============================
    // BUDGET PLAN
    // ===============================

    const budgetPlan =
        document.getElementById("budgetPlan");

    if (budgetPlan) {

        budgetPlan.innerHTML = "";

        if (data.budget_plan) {

            Object.entries(
                data.budget_plan
            ).forEach(([key, value]) => {

                const div =
                    document.createElement("div");

                div.className =
                    "budget-item";

                const span =
                    document.createElement("span");

                span.textContent = key;

                const strong =
                    document.createElement("strong");

                strong.textContent =
                    money(value);

                div.appendChild(span);
                div.appendChild(strong);

                budgetPlan.appendChild(div);
            });
        }
    }


    // ===============================
    // MENU
    // ===============================

    const menu =
        document.getElementById("menu");

    if (menu) {

        menu.innerHTML = "";

        const items =
            Array.isArray(data.menu)
                ? data.menu
                : [];

        items.forEach(item => {

            menu.appendChild(
                createListItem(item)
            );
        });
    }


    // ===============================
    // MUSIC
    // ===============================

    const music =
        document.getElementById("music");

    if (music) {

        music.innerHTML = "";

        const items =
            Array.isArray(data.music_suggestions)
                ? data.music_suggestions
                : [];

        items.forEach(item => {

            music.appendChild(
                createListItem(item)
            );
        });
    }


    // ===============================
    // CHECKLIST
    // ===============================

    const checklist =
        document.getElementById("checklist");

    if (checklist) {

        checklist.innerHTML = "";

        const items =
            Array.isArray(data.checklist)
                ? data.checklist
                : [];

        items.forEach((item, index) => {

            const div =
                document.createElement("div");

            div.className =
                "check-item";

            const number =
                document.createElement("span");

            number.className =
                "number";

            number.textContent =
                index + 1;

            const text =
                document.createElement("span");

            text.textContent = item;

            div.appendChild(number);
            div.appendChild(text);

            checklist.appendChild(div);
        });
    }


    // ===============================
    // TIMELINE
    // ===============================

    const timeline =
        document.getElementById("timeline");

    if (timeline) {

        timeline.innerHTML = "";

        const items =
            Array.isArray(data.timeline)
                ? data.timeline
                : [];

        items.forEach(item => {

            const div =
                document.createElement("div");

            div.className =
                "timeline-item";

            const time =
                document.createElement("strong");

            time.textContent =
                item.time || "";

            const activity =
                document.createElement("span");

            activity.textContent =
                item.activity || "";

            div.appendChild(time);
            div.appendChild(activity);

            timeline.appendChild(div);
        });
    }


    // ===============================
    // SUMMARY
    // ===============================

    const summary =
        document.getElementById("summary");

    if (summary) {

        summary.textContent =
            data.summary ||
            "Your event plan has been generated successfully.";
    }
}


// ===============================
// PAGE LOAD
// ===============================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        // Create page
        const eventText =
            document.getElementById("eventText");

        if (eventText) {

            const button =
                document.getElementById("generateBtn");

            if (button) {

                button.addEventListener(
                    "click",
                    generatePlan
                );
            }
        }


        // Result page
        const resultPage =
            document.getElementById("eventType");

        if (resultPage) {

            const data =
                getData();

            showResult(data);
        }
    }
);

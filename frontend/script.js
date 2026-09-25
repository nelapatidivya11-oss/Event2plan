const API_URL = "/generate";

function getData() {
    try {
        return JSON.parse(localStorage.getItem("eventPlan"));
    } catch {
        return null;
    }
}

function money(value) {
    if (typeof value === "number") {
        return "₹" + value.toLocaleString("en-IN");
    }

    if (value === null || value === undefined || value === "") {
        return "Not specified";
    }

    return value;
}

function createTag(text) {
    const div = document.createElement("div");
    div.className = "tag";
    div.textContent = text;
    return div;
}

function createListItem(text) {
    const div = document.createElement("div");
    div.className = "list-item";
    div.textContent = "✓ " + text;
    return div;
}

function showResult(data) {

    if (!data) {
        document.getElementById("errorBox").textContent =
            "No event data found. Please create an event first.";
        return;
    }

    if (data.error) {
        document.getElementById("errorBox").textContent = data.error;
        return;
    }

    document.getElementById("eventType").textContent =
        data.event_type || "Not specified";

    document.getElementById("people").textContent =
        data.people || "Not specified";

    document.getElementById("location").textContent =
        data.location || "Not specified";

    document.getElementById("budget").textContent =
        money(data.budget);

    const requirements = document.getElementById("requirements");
    requirements.innerHTML = "";

    (data.requirements || []).forEach(item => {
        requirements.appendChild(createTag(item));
    });

    const budgetPlan = document.getElementById("budgetPlan");
    budgetPlan.innerHTML = "";

    if (data.budget_plan) {

        Object.entries(data.budget_plan).forEach(([key, value]) => {

            const div = document.createElement("div");
            div.className = "budget-item";

            div.innerHTML = `
                <span>${key}</span>
                <strong>${money(value)}</strong>
            `;

            budgetPlan.appendChild(div);
        });
    }

    const menu = document.getElementById("menu");
    menu.innerHTML = "";

    (data.menu || []).forEach(item => {
        menu.appendChild(createListItem(item));
    });

    const music = document.getElementById("music");
    music.innerHTML = "";

    (data.music_suggestions || []).forEach(item => {
        music.appendChild(createListItem(item));
    });

    const checklist = document.getElementById("checklist");
    checklist.innerHTML = "";

    (data.checklist || []).forEach((item, index) => {

        const div = document.createElement("div");
        div.className = "check-item";

        div.innerHTML = `
            <span class="number">${index + 1}</span>
            <span>${item}</span>
        `;

        checklist.appendChild(div);
    });

    const timeline = document.getElementById("timeline");
    timeline.innerHTML = "";

    (data.timeline || []).forEach(item => {

        const div = document.createElement("div");
        div.className = "timeline-item";

        div.innerHTML = `
            <strong>${item.time}</strong>
            <span>${item.activity}</span>
        `;

        timeline.appendChild(div);
    });

    document.getElementById("summary").textContent =
        data.summary || "Your event plan has been generated successfully.";
}

document.addEventListener("DOMContentLoaded", showResult);

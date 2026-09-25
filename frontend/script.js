 async function generatePlan() {

    const text = document.getElementById("eventText").value.trim();

    if (!text) {
        alert("Please describe your event first.");
        return;
    }

    const button = document.getElementById("generateBtn");
    const loading = document.getElementById("loading");
    const resultSection = document.getElementById("resultSection");

    button.disabled = true;
    button.innerText = "Generating...";
    loading.classList.remove("hidden");
    resultSection.classList.add("hidden");

    try {

        const response = await fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();

        if (!response.ok || data.error) {
            throw new Error(data.error || "Something went wrong.");
        }

        displayPlan(data);

        resultSection.classList.remove("hidden");

        resultSection.scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {

        console.error(error);

        alert(
            "Unable to generate the plan.\n\n" +
            error.message
        );

    } finally {

        button.disabled = false;
        button.innerText = "✨ Generate Complete Plan";
        loading.classList.add("hidden");
    }
}


function displayPlan(data) {

    document.getElementById("eventType").innerText =
        data.event_type;

    document.getElementById("people").innerText =
        data.people;

    document.getElementById("location").innerText =
        data.location;

    document.getElementById("budget").innerText =
        formatMoney(data.budget);


    // Requirements

    const requirements =
        document.getElementById("requirements");

    requirements.innerHTML = "";

    data.requirements.forEach(item => {

        const tag = document.createElement("div");

        tag.className = "tag";
        tag.innerText = item;

        requirements.appendChild(tag);
    });


    // Budget

    const budgetPlan =
        document.getElementById("budgetPlan");

    budgetPlan.innerHTML = "";

    Object.entries(data.budget_plan).forEach(
        ([name, value]) => {

            const item =
                document.createElement("div");

            item.className = "budget-item";

            item.innerHTML = `
                <span>${name}</span>
                <strong>${formatMoney(value)}</strong>
            `;

            budgetPlan.appendChild(item);
        }
    );


    // Menu

    renderList(
        "menu",
        data.menu
    );


    // Music

    renderList(
        "music",
        data.music_suggestions
    );


    // Checklist

    const checklist =
        document.getElementById("checklist");

    checklist.innerHTML = "";

    data.checklist.forEach(item => {

        const row =
            document.createElement("div");

        row.className = "check-item";

        row.innerHTML = `
            <input type="checkbox">
            <span>${item}</span>
        `;

        checklist.appendChild(row);
    });


    // Timeline

    const timeline =
        document.getElementById("timeline");

    timeline.innerHTML = "";

    data.timeline.forEach(item => {

        const row =
            document.createElement("div");

        row.className = "timeline-item";

        row.innerHTML = `
            <div class="timeline-time">
                ${item.time}
            </div>

            <div>
                ${item.activity}
            </div>
        `;

        timeline.appendChild(row);
    });


    // Summary

    document.getElementById("summary").innerText =
        data.summary;
}


function renderList(elementId, items) {

    const container =
        document.getElementById(elementId);

    container.innerHTML = "";

    items.forEach(item => {

        const div =
            document.createElement("div");

        div.className = "list-item";

        div.innerText = item;

        container.appendChild(div);
    });
}


function formatMoney(value) {

    if (
        value === null ||
        value === undefined ||
        value === "Not specified" ||
        value === "Budget not provided"
    ) {
        return value;
    }

    if (typeof value === "number") {
        return "₹" + value.toLocaleString("en-IN");
    }

    return value;
}

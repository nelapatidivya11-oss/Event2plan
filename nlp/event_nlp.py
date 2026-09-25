import sys
import json
import re


def find_first_number(text, patterns):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None


def detect_event_type(text):
    t = text.lower()

    event_patterns = [
        (r"\bbirthday\b|\bbday\b", "Birthday"),
        (r"\bwedding\b|\bmarriage\b|\bshaadi\b", "Wedding"),
        (r"\breception\b", "Reception"),
        (r"\bengagement\b", "Engagement"),
        (r"\banniversary\b", "Anniversary"),
        (r"\bbaby shower\b|\bbabyshower\b", "Baby Shower"),
        (r"\bbridal shower\b", "Bridal Shower"),
        (r"\bparty\b|\bcelebration\b|\bcelebrate\b", "Party"),
        (r"\bmeeting\b|\bmeetup\b", "Meeting"),
        (r"\bconference\b", "Conference"),
        (r"\bworkshop\b", "Workshop"),
        (r"\bseminar\b", "Seminar"),
        (r"\bwebinar\b", "Webinar"),
        (r"\bfarewell\b", "Farewell"),
        (r"\bgraduation\b|\bconvocation\b", "Graduation"),
        (r"\bhousewarming\b|\bhouse warming\b", "Housewarming"),
        (r"\bcorporate event\b|\bcorporate\b", "Corporate Event"),
        (r"\bsports event\b|\bsports\b", "Sports Event"),
        (r"\bfestival\b", "Festival"),
    ]

    for pattern, event in event_patterns:
        if re.search(pattern, t):
            return event

    return "General Event"


def detect_people(text):
    patterns = [
        r"for\s+(\d+)\s+(?:people|persons|guests|members)",
        r"with\s+(\d+)\s+(?:people|persons|guests|members)",
        r"(\d+)\s+(?:people|persons|guests|members)",
        r"around\s+(\d+)",
        r"about\s+(\d+)",
        r"approximately\s+(\d+)",
        r"attendees?\s*(?:of|:)?\s*(\d+)",
    ]

    return find_first_number(text, patterns)


def detect_budget(text):
    patterns = [
        r"(?:budget|spend|spending|cost|amount)\s*(?:of|is|around|about|:)?\s*(?:₹|rs\.?|inr)?\s*([\d,]+)",
        r"(?:₹|rs\.?|inr)\s*([\d,]+)",
        r"([\d,]+)\s*(?:rupees|rs)\b",
    ]

    value = find_first_number(text, patterns)

    if value:
        return value

    return None


def detect_location(text):
    patterns = [
        r"\bin\s+([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,2})",
        r"\bat\s+([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,2})",
    ]

    # First try common Indian cities
    cities = [
        "Hyderabad", "Vijayawada", "Guntur", "Ongole",
        "Nellore", "Kavali", "Chennai", "Bangalore",
        "Bengaluru", "Mumbai", "Delhi", "Pune",
        "Visakhapatnam", "Vizag", "Tirupati", "Kolkata",
        "Kochi", "Mysore", "Mysuru", "Ahmedabad",
        "Jaipur", "Goa"
    ]

    lower = text.lower()

    for city in cities:
        if city.lower() in lower:
            return city

    # Generic location after "in"
    match = re.search(r"\bin\s+([A-Za-z][A-Za-z\s]{2,30})", text, re.IGNORECASE)

    if match:
        location = match.group(1).strip()

        # Remove common trailing words
        location = re.split(
            r"\b(?:with|for|on|at|and|budget|costing|cost|under)\b",
            location,
            flags=re.IGNORECASE
        )[0].strip()

        if location:
            return location.title()

    return "Not specified"


def detect_requirements(text):
    t = text.lower()

    requirements = []

    requirement_map = {
        "Food": [
            "food", "catering", "meal", "meals",
            "dinner", "lunch", "breakfast"
        ],
        "Decorations": [
            "decoration", "decorations", "decor",
            "balloons", "flowers", "stage decoration"
        ],
        "Music": [
            "music", "songs", "dj", "sound system",
            "speaker", "speakers"
        ],
        "Photography": [
            "photo", "photography", "photographer",
            "photos", "camera"
        ],
        "Videography": [
            "video", "videography", "videographer"
        ],
        "Cake": [
            "cake", "birthday cake"
        ],
        "Venue": [
            "venue", "hall", "function hall",
            "hotel", "banquet"
        ],
        "Games": [
            "games", "game", "activities",
            "fun activities"
        ],
        "Invitations": [
            "invitation", "invitations",
            "invite", "invites"
        ]
    }

    for requirement, keywords in requirement_map.items():
        for keyword in keywords:
            if keyword in t:
                requirements.append(requirement)
                break

    return requirements


def get_menu(event_type, people):
    event = event_type.lower()

    if "birthday" in event or "party" in event:
        menu = [
            "Welcome Drink",
            "Starters",
            "Veg Biryani",
            "Paneer Curry",
            "Dal",
            "Rice",
            "Birthday Cake",
            "Ice Cream"
        ]

    elif "wedding" in event or "reception" in event:
        menu = [
            "Welcome Drink",
            "Starters",
            "Veg Biryani",
            "Paneer Curry",
            "Dal",
            "Sambar",
            "Rice",
            "Sweet",
            "Ice Cream"
        ]

    elif "meeting" in event or "conference" in event or "seminar" in event:
        menu = [
            "Tea",
            "Coffee",
            "Biscuits",
            "Snacks",
            "Lunch"
        ]

    elif "workshop" in event:
        menu = [
            "Tea",
            "Coffee",
            "Snacks",
            "Lunch",
            "Water"
        ]

    else:
        menu = [
            "Welcome Drink",
            "Starters",
            "Main Course",
            "Dessert"
        ]

    return menu


def get_music(event_type):
    event = event_type.lower()

    if "birthday" in event:
        return [
            "Birthday Playlist",
            "DJ Music",
            "Dance Songs",
            "Fun Games"
        ]

    if "wedding" in event or "reception" in event:
        return [
            "Wedding Songs",
            "DJ",
            "Traditional Music",
            "Dance Performance"
        ]

    if "meeting" in event or "conference" in event:
        return [
            "Soft Background Music",
            "Presentation Audio"
        ]

    if "workshop" in event or "seminar" in event:
        return [
            "Soft Background Music",
            "Presentation Audio"
        ]

    return [
        "Background Music",
        "DJ / Playlist",
        "Fun Activities"
    ]


def get_checklist(event_type, requirements):
    checklist = [
        "Finalize event date and time",
        "Confirm guest list",
        "Select and book venue"
    ]

    if "Food" in requirements:
        checklist.append("Arrange food and catering")

    if "Decorations" in requirements:
        checklist.append("Arrange decorations")

    if "Music" in requirements:
        checklist.append("Arrange music and sound system")

    if "Photography" in requirements:
        checklist.append("Book photographer")

    if "Videography" in requirements:
        checklist.append("Arrange videography")

    if "Cake" in requirements:
        checklist.append("Order the cake")

    if "Invitations" in requirements:
        checklist.append("Send invitations")

    if "Games" in requirements:
        checklist.append("Prepare games and activities")

    checklist.append("Final event setup and verification")

    return checklist


def get_timeline(event_type):
    event = event_type.lower()

    if "meeting" in event or "conference" in event or "seminar" in event:
        return [
            {"time": "09:00 AM", "activity": "Guest Arrival & Registration"},
            {"time": "09:30 AM", "activity": "Welcome & Introduction"},
            {"time": "10:00 AM", "activity": "Main Session"},
            {"time": "11:30 AM", "activity": "Break"},
            {"time": "12:00 PM", "activity": "Discussion / Activities"},
            {"time": "01:00 PM", "activity": "Lunch & Closing"}
        ]

    return [
        {"time": "05:00 PM", "activity": "Guest Arrival"},
        {"time": "05:30 PM", "activity": "Welcome"},
        {"time": "06:00 PM", "activity": "Main Event Activity"},
        {"time": "07:00 PM", "activity": "Food & Refreshments"},
        {"time": "08:00 PM", "activity": "Music & Entertainment"},
        {"time": "09:00 PM", "activity": "Closing"}
    ]


def get_budget_plan(budget, event_type):
    if not budget:
        return {
            "Food": "Not specified",
            "Decorations": "Not specified",
            "Music": "Not specified",
            "Venue": "Not specified",
            "Photography": "Not specified",
            "Other": "Not specified",
            "Total": "Budget not provided"
        }

    food = round(budget * 0.35)
    decorations = round(budget * 0.15)
    music = round(budget * 0.10)
    venue = round(budget * 0.20)
    photography = round(budget * 0.10)
    other = budget - (
        food + decorations + music + venue + photography
    )

    return {
        "Food": food,
        "Decorations": decorations,
        "Music": music,
        "Venue": venue,
        "Photography": photography,
        "Other": other,
        "Total": budget
    }


def generate_plan(text):
    event_type = detect_event_type(text)
    people = detect_people(text)
    budget = detect_budget(text)
    location = detect_location(text)
    requirements = detect_requirements(text)

    if not requirements:
        requirements = ["General Arrangements"]

    menu = get_menu(event_type, people)
    music = get_music(event_type)
    checklist = get_checklist(event_type, requirements)
    timeline = get_timeline(event_type)
    budget_plan = get_budget_plan(budget, event_type)

    if people:
        people_text = str(people)
    else:
        people_text = "Not specified"

    return {
        "event_type": event_type,
        "people": people_text,
        "location": location,
        "budget": budget if budget else "Not specified",
        "requirements": requirements,
        "budget_plan": budget_plan,
        "menu": menu,
        "music_suggestions": music,
        "checklist": checklist,
        "timeline": timeline,
        "summary": (
            f"Your {event_type.lower()} is planned for "
            f"{people_text} people in {location}. "
            f"The application generated a budget plan, menu, "
            f"entertainment suggestions, checklist and timeline."
        )
    }


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print(json.dumps({
                "error": "Please provide an event description."
            }))
            sys.exit(0)

        text = " ".join(sys.argv[1:]).strip()

        result = generate_plan(text)

        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({
            "error": str(e)
        }))

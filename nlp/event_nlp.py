import sys
import json
import re


def extract_number(text):
    if not text:
        return None

    match = re.search(r"\d[\d,]*", text)

    if match:
        return int(match.group(0).replace(",", ""))

    return None


def detect_event_type(text):
    t = text.lower()

    patterns = [
        (r"\bbirthday\b|\bbday\b", "Birthday"),
        (r"\bwedding\b|\bmarriage\b|\bshaadi\b", "Wedding"),
        (r"\breception\b", "Reception"),
        (r"\bengagement\b", "Engagement"),
        (r"\banniversary\b", "Anniversary"),
        (r"\bbaby\s*shower\b", "Baby Shower"),
        (r"\bbridal\s*shower\b", "Bridal Shower"),
        (r"\bparty\b|\bcelebration\b|\bcelebrate\b", "Party"),
        (r"\bmeeting\b|\bmeetup\b", "Meeting"),
        (r"\bconference\b", "Conference"),
        (r"\bworkshop\b", "Workshop"),
        (r"\bseminar\b", "Seminar"),
        (r"\bwebinar\b", "Webinar"),
        (r"\bfarewell\b", "Farewell"),
        (r"\bgraduation\b|\bconvocation\b", "Graduation"),
        (r"\bhousewarming\b|\bhouse\s*warming\b", "Housewarming"),
        (r"\bcorporate\s*event\b|\bcorporate\b", "Corporate Event"),
        (r"\bsports\s*event\b|\bsports\b", "Sports Event"),
        (r"\bfestival\b", "Festival")
    ]

    for pattern, event in patterns:
        if re.search(pattern, t):
            return event

    return "General Event"


def detect_people(text):
    patterns = [
        r"(\d[\d,]*)\s*(?:people|persons|guests|members|attendees)",
        r"(?:for|with|around|about|approximately)\s+(\d[\d,]*)",
        r"(?:guest|guests|people|persons|attendees)\s*(?:of|:)?\s*(\d[\d,]*)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return int(match.group(1).replace(",", ""))

    return None


def detect_budget(text):
    patterns = [
        r"(?:budget|cost|amount|spend|spending)\s*(?:is|of|around|about|:)?\s*(?:₹|rs\.?|inr)?\s*([\d,]+)",
        r"(?:₹|rs\.?|inr)\s*([\d,]+)",
        r"([\d,]+)\s*(?:rupees|rs)\b",
        r"([\d,]+)\s*(?:budget)\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return int(match.group(1).replace(",", ""))

    return None


def detect_location(text):
    cities = [
        "Hyderabad",
        "Vijayawada",
        "Guntur",
        "Ongole",
        "Nellore",
        "Kavali",
        "Chennai",
        "Bangalore",
        "Bengaluru",
        "Mumbai",
        "Delhi",
        "Pune",
        "Visakhapatnam",
        "Vizag",
        "Tirupati",
        "Kolkata",
        "Kochi",
        "Mysore",
        "Mysuru",
        "Ahmedabad",
        "Jaipur",
        "Goa"
    ]

    lower = text.lower()

    for city in cities:
        if city.lower() in lower:
            return city

    patterns = [
        r"\bin\s+([A-Za-z]+(?:\s+[A-Za-z]+){0,2})",
        r"\bat\s+([A-Za-z]+(?:\s+[A-Za-z]+){0,2})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            location = match.group(1).strip()

            location = re.split(
                r"\b(?:with|for|on|at|and|budget|cost|under)\b",
                location,
                flags=re.IGNORECASE
            )[0].strip()

            if location:
                return location.title()

    return "Not specified"


def detect_requirements(text):
    t = text.lower()

    requirement_map = {
        "Food": [
            "food",
            "catering",
            "meal",
            "meals",
            "dinner",
            "lunch",
            "breakfast"
        ],

        "Decorations": [
            "decoration",
            "decorations",
            "decor",
            "balloons",
            "flowers",
            "flower",
            "stage decoration"
        ],

        "Music": [
            "music",
            "songs",
            "song",
            "dj",
            "sound system",
            "speaker",
            "speakers"
        ],

        "Photography": [
            "photo",
            "photos",
            "photography",
            "photographer",
            "camera"
        ],

        "Videography": [
            "video",
            "videos",
            "videography",
            "videographer"
        ],

        "Cake": [
            "cake"
        ],

        "Venue": [
            "venue",
            "hall",
            "function hall",
            "hotel",
            "banquet"
        ],

        "Games": [
            "game",
            "games",
            "activity",
            "activities"
        ],

        "Invitations": [
            "invitation",
            "invitations",
            "invite",
            "invites"
        ]
    }

    requirements = []

    for requirement, keywords in requirement_map.items():

        for keyword in keywords:

            if keyword in t:
                requirements.append(requirement)
                break

    return requirements


def get_menu(event_type):

    event = event_type.lower()

    if "birthday" in event or "party" in event:
        return [
            "Welcome Drink",
            "Starters",
            "Veg Biryani",
            "Paneer Curry",
            "Dal",
            "Rice",
            "Birthday Cake",
            "Ice Cream"
        ]

    if "wedding" in event or "reception" in event:
        return [
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

    if (
        "meeting" in event
        or "conference" in event
        or "seminar" in event
    ):
        return [
            "Tea",
            "Coffee",
            "Biscuits",
            "Snacks",
            "Lunch"
        ]

    if "workshop" in event:
        return [
            "Tea",
            "Coffee",
            "Snacks",
            "Lunch",
            "Water"
        ]

    return [
        "Welcome Drink",
        "Starters",
        "Main Course",
        "Dessert"
    ]


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


def get_checklist(requirements):

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

    if (
        "meeting" in event
        or "conference" in event
        or "seminar" in event
        or "workshop" in event
    ):
        return [
            {
                "time": "09:00 AM",
                "activity": "Guest Arrival & Registration"
            },
            {
                "time": "09:30 AM",
                "activity": "Welcome & Introduction"
            },
            {
                "time": "10:00 AM",
                "activity": "Main Session"
            },
            {
                "time": "11:30 AM",
                "activity": "Break"
            },
            {
                "time": "12:00 PM",
                "activity": "Discussion / Activities"
            },
            {
                "time": "01:00 PM",
                "activity": "Lunch & Closing"
            }
        ]

    return [
        {
            "time": "05:00 PM",
            "activity": "Guest Arrival"
        },
        {
            "time": "05:30 PM",
            "activity": "Welcome"
        },
        {
            "time": "06:00 PM",
            "activity": "Main Event Activity"
        },
        {
            "time": "07:00 PM",
            "activity": "Food & Refreshments"
        },
        {
            "time": "08:00 PM",
            "activity": "Music & Entertainment"
        },
        {
            "time": "09:00 PM",
            "activity": "Closing"
        }
    ]


def get_budget_plan(budget):

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
        food
        + decorations
        + music
        + venue
        + photography
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

    people_text = (
        str(people)
        if people is not None
        else "Not specified"
    )

    return {
        "event_type": event_type,

        "people": people_text,

        "location": location,

        "budget": (
            budget
            if budget is not None
            else "Not specified"
        ),

        "requirements": requirements,

        "budget_plan": get_budget_plan(budget),

        "menu": get_menu(event_type),

        "music_suggestions": get_music(event_type),

        "checklist": get_checklist(requirements),

        "timeline": get_timeline(event_type),

        "summary": (
            f"Your {event_type.lower()} is planned for "
            f"{people_text} people in {location}. "
            f"The application generated a smart budget plan, "
            f"menu suggestions, entertainment suggestions, "
            f"checklist and event timeline."
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

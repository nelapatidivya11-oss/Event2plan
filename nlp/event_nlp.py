import sys
import json
import re


# =========================================================
# EVENT TYPE DETECTION
# =========================================================

def find_event_type(text):

    t = text.lower().strip()

    # Order matters: specific events first
    if any(word in t for word in [
        "birthday",
        "bday",
        "birth day",
        "birthday party"
    ]):
        return "Birthday Party"

    if any(word in t for word in [
        "wedding",
        "marriage",
        "marry",
        "wedding ceremony"
    ]):
        return "Wedding"

    if any(word in t for word in [
        "engagement",
        "engage",
        "engagement ceremony"
    ]):
        return "Engagement"

    if "reception" in t:
        return "Reception"

    if "baby shower" in t:
        return "Baby Shower"

    if any(word in t for word in [
        "anniversary",
        "anniversary party"
    ]):
        return "Anniversary"

    if any(word in t for word in [
        "farewell party",
        "farewell",
        "send off",
        "send-off"
    ]):
        return "Farewell Party"

    if any(word in t for word in [
        "welcome party",
        "welcome event"
    ]):
        return "Welcome Party"

    if any(word in t for word in [
        "meeting",
        "meetup",
        "discussion",
        "business meeting"
    ]):
        return "Meeting"

    if any(word in t for word in [
        "workshop",
        "training",
        "training program"
    ]):
        return "Workshop"

    if any(word in t for word in [
        "seminar",
        "seminar program"
    ]):
        return "Seminar"

    if any(word in t for word in [
        "conference",
        "conference meeting"
    ]):
        return "Conference"

    if any(word in t for word in [
        "college event",
        "college fest",
        "college function",
        "college program",
        "campus event",
        "campus program",
        "college celebration"
    ]):
        return "College Event"

    if any(word in t for word in [
        "party",
        "celebration",
        "celebrate",
        "function",
        "event"
    ]):
        return "Party"

    return "Custom Event"


# =========================================================
# NUMBER OF PEOPLE
# =========================================================

def find_people(text):

    t = text.lower()

    patterns = [

        r"(\d+)\s*(?:people|persons|person|guests|guest|members|students|attendees)",

        r"(?:for|with)\s*(?:around|about|nearly|approximately)?\s*(\d+)",

        r"(\d+)\s*(?:of us|of people)"
    ]

    for pattern in patterns:

        match = re.search(pattern, t)

        if match:
            return match.group(1)

    return "Not specified"


# =========================================================
# BUDGET
# =========================================================

def find_budget(text):

    t = text.lower()

    patterns = [

        r"(?:budget|cost|amount)\s*(?:of|is|around|about)?\s*(?:₹|rs\.?|inr)?\s*([\d,]+)",

        r"(?:₹|rs\.?|inr)\s*([\d,]+)"
    ]

    for pattern in patterns:

        match = re.search(pattern, t)

        if match:
            return "₹" + match.group(1)

    return "Not specified"


# =========================================================
# LOCATION
# =========================================================

def find_location(text):

    # Common Indian cities / locations
    locations = [
        "Hyderabad",
        "Bangalore",
        "Bengaluru",
        "Chennai",
        "Mumbai",
        "Delhi",
        "Kolkata",
        "Pune",
        "Vijayawada",
        "Nellore",
        "Kavali",
        "Tirupati",
        "Visakhapatnam",
        "Vizag",
        "Guntur",
        "Warangal",
        "Kochi",
        "Goa"
    ]

    for location in locations:

        if re.search(
            r"\b" + re.escape(location) + r"\b",
            text,
            re.IGNORECASE
        ):
            return location

    return "Not specified"


# =========================================================
# REQUIREMENTS
# =========================================================

def find_requirements(text):

    t = text.lower()

    requirements = []

    keywords = {

        "Food": [
            "food",
            "catering",
            "meal",
            "meals",
            "lunch",
            "dinner",
            "breakfast",
            "refreshments",
            "menu"
        ],

        "Decorations": [
            "decoration",
            "decorations",
            "decor",
            "flowers",
            "balloons",
            "lights",
            "lighting"
        ],

        "Music": [
            "music",
            "songs",
            "song",
            "dj",
            "dance",
            "sound",
            "speaker"
        ],

        "Cake": [
            "cake"
        ],

        "Photography": [
            "photo",
            "photos",
            "photography",
            "photographer",
            "video",
            "videography",
            "videographer"
        ],

        "Venue": [
            "venue",
            "hall",
            "location",
            "auditorium",
            "hotel",
            "resort",
            "place"
        ],

        "Invitation": [
            "invitation",
            "invitations",
            "invite",
            "invites"
        ],

        "Games": [
            "games",
            "game",
            "activities",
            "activity"
        ],

        "Transport": [
            "transport",
            "transportation",
            "bus",
            "vehicle",
            "travel"
        ]
    }

    for requirement, words in keywords.items():

        for word in words:

            if word in t:
                requirements.append(requirement)
                break

    # Default requirements
    if not requirements:

        requirements = [
            "Venue",
            "Guest arrangements",
            "Food and refreshments",
            "Event schedule"
        ]

    return requirements


# =========================================================
# MENU GENERATION
# =========================================================

def generate_menu(event_type):

    if event_type == "Birthday Party":

        return [
            "Welcome Drink",
            "Veg Biryani",
            "Paneer Curry",
            "Fried Rice",
            "Gobi Manchurian",
            "Salad",
            "Birthday Cake",
            "Ice Cream"
        ]

    if event_type in [
        "Wedding",
        "Reception",
        "Engagement"
    ]:

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

    if event_type == "Baby Shower":

        return [
            "Welcome Drink",
            "Snacks",
            "Vegetable Biryani",
            "Paneer Curry",
            "Fruits",
            "Sweet",
            "Cake"
        ]

    if event_type == "Anniversary":

        return [
            "Welcome Drink",
            "Starters",
            "Biryani",
            "Paneer Curry",
            "Fried Rice",
            "Salad",
            "Cake",
            "Ice Cream"
        ]

    if event_type == "Farewell Party":

        return [
            "Welcome Drink",
            "Snacks",
            "Starters",
            "Biryani",
            "Main Course",
            "Dessert",
            "Ice Cream"
        ]

    if event_type in [
        "Meeting",
        "Workshop",
        "Seminar",
        "Conference"
    ]:

        return [
            "Tea",
            "Coffee",
            "Biscuits",
            "Snacks",
            "Lunch",
            "Fruit Juice"
        ]

    if event_type == "College Event":

        return [
            "Welcome Drink",
            "Snacks",
            "Veg Biryani",
            "Fried Rice",
            "Paneer Curry",
            "Soft Drinks",
            "Ice Cream"
        ]

    return [
        "Welcome Drink",
        "Starters",
        "Main Course",
        "Rice/Biryani",
        "Dessert",
        "Ice Cream"
    ]


# =========================================================
# MUSIC GENERATION
# =========================================================

def generate_music(event_type):

    if event_type == "Birthday Party":

        return [
            "Birthday Celebration Songs",
            "Popular Party Songs",
            "Dance Music",
            "DJ Party Mix"
        ]

    if event_type in [
        "Wedding",
        "Reception",
        "Engagement"
    ]:

        return [
            "Wedding Entry Music",
            "Romantic Songs",
            "Traditional Music",
            "Dance Songs"
        ]

    if event_type == "Baby Shower":

        return [
            "Soft Celebration Music",
            "Family Songs",
            "Happy Background Music"
        ]

    if event_type == "Anniversary":

        return [
            "Romantic Songs",
            "Couple Celebration Songs",
            "Soft Background Music",
            "Dance Music"
        ]

    if event_type == "Farewell Party":

        return [
            "Farewell Songs",
            "Friendship Songs",
            "Memories Songs",
            "Dance Music"
        ]

    if event_type == "College Event":

        return [
            "Popular Songs",
            "DJ Music",
            "Dance Music",
            "College Celebration Songs"
        ]

    if event_type in [
        "Meeting",
        "Workshop",
        "Seminar",
        "Conference"
    ]:

        return [
            "Soft Background Music",
            "Instrumental Music"
        ]

    return [
        "Popular Songs",
        "Background Music",
        "Celebration Music"
    ]


# =========================================================
# DECORATION GENERATION
# =========================================================

def generate_decorations(event_type):

    if event_type == "Birthday Party":

        return [
            "Balloons",
            "Event Banner",
            "Colorful Lights",
            "Photo Booth",
            "Table Decorations"
        ]

    if event_type in [
        "Wedding",
        "Reception",
        "Engagement"
    ]:

        return [
            "Flower Decorations",
            "Stage Decoration",
            "Fairy Lights",
            "Entrance Decoration",
            "Table Decorations"
        ]

    if event_type == "Baby Shower":

        return [
            "Baby Theme Decorations",
            "Balloons",
            "Flower Decorations",
            "Photo Booth",
            "Welcome Board"
        ]

    if event_type == "Anniversary":

        return [
            "Flower Decorations",
            "Romantic Lights",
            "Photo Wall",
            "Table Decorations",
            "Welcome Board"
        ]

    if event_type == "Farewell Party":

        return [
            "Farewell Banner",
            "Photo Wall",
            "Balloons",
            "Memory Board",
            "Stage Decoration"
        ]

    if event_type == "College Event":

        return [
            "College Banner",
            "Stage Setup",
            "Colorful Lights",
            "Photo Booth",
            "Entrance Decoration"
        ]

    if event_type in [
        "Meeting",
        "Workshop",
        "Seminar",
        "Conference"
    ]:

        return [
            "Stage Setup",
            "Event Banner",
            "Lighting",
            "Seating Arrangement"
        ]

    return [
        "Balloons",
        "Lights",
        "Event Banner",
        "Table Decorations",
        "Entrance Decoration"
    ]


# =========================================================
# CHECKLIST
# =========================================================

def generate_checklist(requirements):

    checklist = [
        "Finalize event date and time",
        "Confirm venue",
        "Prepare guest list"
    ]

    if "Food" in requirements:

        checklist.append(
            "Arrange food and catering"
        )

    if "Decorations" in requirements:

        checklist.append(
            "Arrange decorations"
        )

    if "Music" in requirements:

        checklist.append(
            "Arrange music and sound system"
        )

    if "Photography" in requirements:

        checklist.append(
            "Arrange photography and videography"
        )

    if "Invitation" in requirements:

        checklist.append(
            "Send invitations"
        )

    if "Games" in requirements:

        checklist.append(
            "Prepare games and activities"
        )

    if "Transport" in requirements:

        checklist.append(
            "Arrange transportation"
        )

    checklist.append(
        "Confirm all arrangements before the event"
    )

    return checklist


# =========================================================
# MAIN EVENT ANALYSIS
# =========================================================

def analyze_event(text):

    event_type = find_event_type(text)

    people = find_people(text)

    budget = find_budget(text)

    location = find_location(text)

    requirements = find_requirements(text)

    result = {

        "event_type": event_type,

        "people": people,

        "budget": budget,

        "location": location,

        "requirements": requirements,

        "menu": generate_menu(event_type),

        "music": generate_music(event_type),

        "decorations": generate_decorations(event_type),

        "checklist": generate_checklist(requirements)
    }

    return result


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(json.dumps({
            "error": "Please provide an event description."
        }))

        sys.exit(1)

    text = " ".join(sys.argv[1:])

    result = analyze_event(text)

    print(json.dumps(result))
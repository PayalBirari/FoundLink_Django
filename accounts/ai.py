
import re


def ask_foundlink_ai(message):
    """Rule-based FoundLink Assistant without Gemini."""

    if not isinstance(message, str):
        return "Please enter your question as text."

    question = message.strip().lower()
    words = set(re.findall(r"[a-z]+", question))

    if not question:
        return "Hello! I am FoundLink Assistant. How can I help you?"

    # 1. Greetings
    if words.intersection({"hello", "hi", "hey", "hii"}):
        return (
            "Hello! Welcome to FoundLink. I can help you report lost or "
            "found items, understand Smart Match, and use the website."
        )

    # 2. Thank you
    if words.intersection({"thank", "thanks"}):
        return (
            "You're welcome! I am happy to help you use FoundLink. "
            "Feel free to ask me another question."
        )

    # 3. Who are you?
    if "who are you" in question or "who are you" in question.replace("?", ""):
        return (
            "I am FoundLink Assistant, a built-in helper for the FoundLink "
            "Lost and Found Management System."
        )

    # 4. What is FoundLink?
    if "foundlink" in words and words.intersection(
        {"what", "purpose", "about", "explain", "is"}
    ):
        return (
            "FoundLink is a Lost and Found Management System that helps "
            "people report lost items, report found items, identify possible "
            "matches using Smart Match, receive notifications, and connect "
            "with other users to help return lost belongings."
        )

    # 5. Purpose of FoundLink
    if "purpose" in words:
        return (
            "The purpose of FoundLink is to make it easier to report lost "
            "belongings, register found items, identify possible matches, "
            "and help items return to their rightful owners."
        )

    # 6. Features of FoundLink
    if words.intersection({"features", "feature", "functionality"}):
        return (
            "FoundLink provides these features:\n"
            "1. Report Lost: Register an item you have lost.\n"
            "2. Report Found: Register an item you have found.\n"
            "3. Smart Match: Identify possible lost-and-found matches.\n"
            "4. Notifications: Receive relevant updates.\n"
            "5. My Reports: View and manage submitted reports.\n"
            "6. Find Users and My Connections: Connect with other users."
        )

    # 7. Recovering a lost item - before general lost-item questions
    if words.intersection(
        {"recover", "recovery", "recovered", "retrieve", "retrieved"}
    ) or "get my item back" in question:
        return (
            "To recover your lost item:\n"
            "1. Open your FoundLink dashboard.\n"
            "2. Check notifications for possible matches.\n"
            "3. Compare the item details in the matching report.\n"
            "4. Use available connection options to contact the user.\n"
            "5. Verify the item and arrange a safe return.\n"
            "Update the item's status after receiving it, if that option "
            "is available."
        )

    # 8. Smart Match
    if words.intersection({"smart", "match", "matching"}):
        return (
            "Smart Match compares lost and found reports using details "
            "such as item name, category, location, and description. "
            "It identifies possible matches and may notify the item's owner. "
            "Always verify the details before arranging a return."
        )

    # 9. Reporting a lost item
    if "lost" in words and words.intersection(
        {"report", "item", "phone", "wallet", "bag", "keys", "belonging"}
    ):
        return (
            "To report a lost item:\n"
            "1. Open Report Lost.\n"
            "2. Enter the item's name, category, location, date, "
            "and description.\n"
            "3. Add a photo if available.\n"
            "4. Submit your report.\n"
            "Check your dashboard for possible matches."
        )

    # 10. Reporting a found item
    if "found" in words and words.intersection(
        {"report", "item", "phone", "wallet", "bag", "keys", "belonging"}
    ):
        return (
            "To report a found item:\n"
            "1. Open Report Found.\n"
            "2. Enter the item's details and where you found it.\n"
            "3. Add a photo if available.\n"
            "4. Submit your report."
        )

    # 11. Uploading photos
    if words.intersection(
        {"photo", "photos", "image", "images", "picture", "pictures", "upload"}
    ):
        return (
            "To upload a photo, open Report Lost or Report Found. Select "
            "a clear image in the photo field, complete the item details, "
            "and submit the form. If uploading fails, check the file type "
            "and size."
        )

    # 12. Notifications
    if words.intersection(
        {"notification", "notifications", "alert", "alerts"}
    ):
        return (
            "Open your FoundLink dashboard to check notifications. They may "
            "include possible item matches, connection requests, and updates."
        )

    # 13. Connecting with users
    if words.intersection(
        {"connection", "connections", "connect", "contact"}
    ):
        return (
            "Open Find Users to search for another FoundLink user. Send a "
            "connection request and view accepted connections under "
            "My Connections."
        )

    # 14. Resetting a password
    if words.intersection(
        {"password", "reset", "forgot", "login", "signin"}
    ):
        return (
            "To reset your password, open the login page and select "
            "Forgot Password. Follow the verification instructions shown "
            "on your website. Never share your password or OTP."
        )

    # 15. Dashboard
    if "dashboard" in words:
        return (
            "The FoundLink dashboard helps you view your activity and "
            "notifications. Check it for possible item matches and updates. "
            "Open My Reports to manage the items you submitted."
        )

    # 16. Staying safe
    if words.intersection(
        {"safe", "safety", "scam", "stranger", "secure"}
    ):
        return (
            "Stay safe when recovering an item. Never share passwords or "
            "OTPs. Verify the claimant, protect your personal details, "
            "and arrange the return in a safe public place. Ask campus "
            "security for help if anything feels suspicious."
        )

    # Default answer
    return (
        "I can help with FoundLink questions about its purpose, features, "
        "lost and found reports, Smart Match, photos, notifications, "
        "connections, passwords, dashboard, and safety. Please try asking "
        "about one of these topics."
    )

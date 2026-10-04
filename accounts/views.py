# =================================================
# IMPORTS
# =================================================

import random

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse

from .forms import RegisterForm, LostItemForm, FoundItemForm

from .models import (
    User,
    LostItem,
    FoundItem,
    Notification,
    Like,
    Comment,
    Connection,
)


# =================================================
# HOME
# =================================================

def home(request):
    return render(request, "home.html")


# =================================================
# REGISTER
# =================================================

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            user.password = make_password(user.password)
            user.save()

            return redirect("home")

    else:

        form = RegisterForm()

    return render(request, "register.html", {
        "form": form
    })


# =================================================
# LOGIN
# =================================================

def login(request):

    if request.method == "POST":

        # Get and clean the values from the login form.
        email = (request.POST.get("email") or "").strip()
        password = request.POST.get("password") or ""

        # Do not allow an empty login request.
        if not email or not password:
            return render(request, "login.html", {
                "error": "Please enter your email and password."
            })

        try:
            # Use case-insensitive email matching so that
            # Payal@Example.com and payal@example.com work the same way.
            user = User.objects.get(email__iexact=email)

            # Check the password against the hashed password stored in DB.
            if check_password(password, user.password):

                # Store the custom FoundLink session values used
                # throughout the rest of the project.
                request.session["user_id"] = user.id
                request.session["user_name"] = user.full_name

                # Make sure the session is saved before redirecting.
                request.session.modified = True

                return redirect("dashboard")

            return render(request, "login.html", {
                "error": "Invalid email or password."
            })

        except User.DoesNotExist:

            return render(request, "login.html", {
                "error": "Invalid email or password."
            })

    return render(request, "login.html")


# =================================================
# FORGOT PASSWORD
# =================================================

def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        try:

            user = User.objects.get(email=email)

            otp = random.randint(100000, 999999)

            request.session["reset_email"] = email
            request.session["reset_otp"] = str(otp)
            request.session["otp_verified"] = False

            print("========================================")
            print("PASSWORD RESET OTP")
            print("EMAIL:", email)
            print("OTP:", otp)
            print("========================================")

            send_mail(
                "FoundLink Password Reset OTP",
                f"Your FoundLink password reset OTP is: {otp}",
                None,
                [email],
                fail_silently=False,
            )

            return redirect("verify_otp")

        except User.DoesNotExist:

            return render(request, "forgot_password.html", {
                "error": "Email address not found."
            })

    return render(request, "forgot_password.html")


# =================================================
# VERIFY OTP
# =================================================

def verify_otp(request):

    if "reset_email" not in request.session:

        return redirect("forgot_password")

    if request.method == "POST":

        entered_otp = request.POST.get("otp")
        saved_otp = request.session.get("reset_otp")

        if entered_otp == saved_otp:

            request.session["otp_verified"] = True

            return redirect("reset_password")

        else:

            return render(request, "verify_otp.html", {
                "error": "Invalid OTP."
            })

    return render(request, "verify_otp.html")


# =================================================
# RESET PASSWORD
# =================================================

def reset_password(request):

    if not request.session.get("otp_verified"):

        return redirect("forgot_password")

    if request.method == "POST":

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            return render(request, "reset_password.html", {
                "error": "Passwords do not match."
            })

        email = request.session.get("reset_email")

        try:

            user = User.objects.get(email=email)

            user.password = make_password(password)
            user.save()

            request.session.pop("reset_email", None)
            request.session.pop("reset_otp", None)
            request.session.pop("otp_verified", None)

            return redirect("login")

        except User.DoesNotExist:

            return redirect("forgot_password")

    return render(request, "reset_password.html")


# =================================================
# LOGOUT
# =================================================

def logout(request):

    print("########## FOUNDLINK LOGOUT VIEW CALLED ##########")

    request.session.flush()

    return redirect("home")


# =================================================
# DASHBOARD
# =================================================

def dashboard(request):

    if "user_id" not in request.session:

        return redirect("login")

    lost_items = LostItem.objects.all().order_by("-created_at")

    found_items = FoundItem.objects.all().order_by("-created_at")

    notifications = []

    lost_count = LostItem.objects.count()

    found_count = FoundItem.objects.count()

    connections_count = 0

    user_id = request.session["user_id"]

    notifications = Notification.objects.filter(
        user_id=user_id
    ).order_by("-created_at")

    connections_count = Connection.objects.filter(
        Q(sender_id=user_id) | Q(receiver_id=user_id),
        status="accepted"
    ).count()

    return render(request, "dashboard.html", {

        "lost_items": lost_items,

        "found_items": found_items,

        "notifications": notifications,

        "lost_count": lost_count,

        "found_count": found_count,

        "connections_count": connections_count,
    })


# =================================================
# CREATE LOST ITEM
# =================================================

def create_lost_item(request):

    if "user_id" not in request.session:

        return redirect("login")

    if request.method == "POST":

        form = LostItemForm(request.POST, request.FILES)

        if form.is_valid():

            item = form.save(commit=False)

            item.user_id = request.session["user_id"]

            item.save()

            print("========================================")
            print("LOST ITEM ADDED SUCCESSFULLY!")
            print("Item:", item.item_name)
            print("Category:", item.category)
            print("Location:", item.location)
            print("========================================")

            return redirect("dashboard")

    else:

        form = LostItemForm()

    return render(request, "add_lost_item.html", {
        "form": form
    })


# =================================================
# VIEW LOST ITEMS
# =================================================

def view_lost_items(request):

    query = request.GET.get("q", "")

    if query:

        lost_items = LostItem.objects.filter(
            Q(item_name__icontains=query) |
            Q(category__icontains=query) |
            Q(location__icontains=query)
        ).order_by("-created_at")

    else:

        lost_items = LostItem.objects.all().order_by("-created_at")

    return render(request, "view_lost_items.html", {
        "lost_items": lost_items,
        "query": query
    })


# =================================================
# VIEW FOUND ITEMS
# =================================================

def view_found_items(request):

    query = request.GET.get("q", "")

    if query:

        found_items = FoundItem.objects.filter(
            Q(item_name__icontains=query) |
            Q(category__icontains=query) |
            Q(location__icontains=query)
        ).order_by("-created_at")

    else:

        found_items = FoundItem.objects.all().order_by("-created_at")

    return render(request, "view_found_items.html", {
        "found_items": found_items,
        "query": query
    })


# =================================================
# CREATE FOUND ITEM + SMART MATCH
# =================================================

def create_found_item(request):

    if "user_id" not in request.session:

        return redirect("login")

    if request.method == "POST":

        form = FoundItemForm(request.POST, request.FILES)

        if form.is_valid():

            item = form.save(commit=False)

            item.user_id = request.session["user_id"]

            item.save()

            print("========================================")
            print("FOUND ITEM ADDED SUCCESSFULLY!")
            print("Item:", item.item_name)
            print("Category:", item.category)
            print("Location:", item.location)
            print("========================================")

            # =========================================
            # SMART MATCH
            # =========================================

            lost_items = LostItem.objects.filter(
                category__iexact=item.category,
                status__in=["lost", "possible_match"]
            )

            for lost_item in lost_items:

                score = 0

                found_name = item.item_name.lower()
                lost_name = lost_item.item_name.lower()

                found_location = item.location.lower()
                lost_location = lost_item.location.lower()

                found_description = item.description.lower()
                lost_description = lost_item.description.lower()

                # ITEM NAME MATCH
                if (
                    found_name in lost_name
                    or lost_name in found_name
                ):

                    score += 3

                # LOCATION MATCH
                if (
                    found_location in lost_location
                    or lost_location in found_location
                ):

                    score += 2

                # DESCRIPTION MATCH
                if (
                    found_description in lost_description
                    or lost_description in found_description
                ):

                    score += 1

                # =====================================
                # MATCH FOUND
                # =====================================

                if score >= 3:

                    lost_item.status = "possible_match"

                    lost_item.save()

                    Notification.objects.create(

                        user=lost_item.user,

                        message=(
                            f"Possible match found for your lost "
                            f"item '{lost_item.item_name}'. "
                            f"A found item '{item.item_name}' "
                            f"was reported at {item.location}."
                        )
                    )

                    print("========================================")
                    print("SMART MATCH FOUND!")
                    print("LOST ITEM:", lost_item.item_name)
                    print("FOUND ITEM:", item.item_name)
                    print("MATCH SCORE:", score)
                    print("NOTIFICATION CREATED")
                    print("NOTIFICATION FOR:", lost_item.user.email)
                    print("========================================")

                    # =================================
                    # EMAIL ALERT
                    # =================================

                    try:

                        send_mail(

                            "FoundLink - Possible Match Found",

                            (
                                f"Possible match found for your lost "
                                f"item '{lost_item.item_name}'.\n\n"

                                f"Found item: {item.item_name}\n"
                                f"Category: {item.category}\n"
                                f"Location: {item.location}\n\n"

                                f"Please check your FoundLink dashboard."
                            ),

                            None,

                            [lost_item.user.email],

                            fail_silently=False,
                        )

                        print("EMAIL ALERT SENT")

                    except Exception as e:

                        print("EMAIL ERROR:", e)

            return redirect("dashboard")

    else:

        form = FoundItemForm()

    return render(request, "add_found_item.html", {
        "form": form
    })


# =================================================
# DELETE LOST ITEM
# =================================================

def delete_lost_item(request, item_id):

    if "user_id" not in request.session:

        return redirect("login")

    try:

        item = LostItem.objects.get(
            id=item_id,
            user_id=request.session["user_id"]
        )

        item.delete()

    except LostItem.DoesNotExist:

        pass

    return redirect("my_reports")


# =================================================
# DELETE FOUND ITEM
# =================================================

def delete_found_item(request, item_id):

    if "user_id" not in request.session:

        return redirect("login")

    try:

        item = FoundItem.objects.get(
            id=item_id,
            user_id=request.session["user_id"]
        )

        item.delete()

    except FoundItem.DoesNotExist:

        pass

    return redirect("my_reports")


# =================================================
# EDIT LOST ITEM
# =================================================

def edit_lost_item(request, item_id):

    if "user_id" not in request.session:

        return redirect("login")

    try:

        item = LostItem.objects.get(
            id=item_id,
            user_id=request.session["user_id"]
        )

    except LostItem.DoesNotExist:

        return redirect("my_reports")

    if request.method == "POST":

        form = LostItemForm(
            request.POST,
            request.FILES,
            instance=item
        )

        if form.is_valid():

            form.save()

            return redirect("my_reports")

    else:

        form = LostItemForm(instance=item)

    return render(request, "edit_lost_item.html", {
        "form": form,
        "item": item
    })


# =================================================
# EDIT FOUND ITEM
# =================================================

def edit_found_item(request, item_id):

    if "user_id" not in request.session:

        return redirect("login")

    try:

        item = FoundItem.objects.get(
            id=item_id,
            user_id=request.session["user_id"]
        )

    except FoundItem.DoesNotExist:

        return redirect("my_reports")

    if request.method == "POST":

        form = FoundItemForm(
            request.POST,
            request.FILES,
            instance=item
        )

        if form.is_valid():

            form.save()

            return redirect("my_reports")

    else:

        form = FoundItemForm(instance=item)

    return render(request, "edit_found_item.html", {
        "form": form,
        "item": item
    })


# =================================================
# DELETE NOTIFICATION
# =================================================

def delete_notification(request, notification_id):

    if "user_id" not in request.session:

        return redirect("login")

    try:

        notification = Notification.objects.get(
            id=notification_id,
            user_id=request.session["user_id"]
        )

        notification.delete()

    except Notification.DoesNotExist:

        pass

    return redirect("dashboard")


# =================================================
# LIKE POST
# =================================================

def like_post(request, item_type, item_id):

    if "user_id" not in request.session:

        return redirect("login")

    user_id = request.session["user_id"]

    if item_type == "lost":

        try:

            item = LostItem.objects.get(id=item_id)

            existing_like = Like.objects.filter(
                user_id=user_id,
                lost_item=item
            ).first()

            if existing_like:

                existing_like.delete()

            else:

                Like.objects.create(
                    user_id=user_id,
                    lost_item=item
                )

        except LostItem.DoesNotExist:

            pass

    elif item_type == "found":

        try:

            item = FoundItem.objects.get(id=item_id)

            existing_like = Like.objects.filter(
                user_id=user_id,
                found_item=item
            ).first()

            if existing_like:

                existing_like.delete()

            else:

                Like.objects.create(
                    user_id=user_id,
                    found_item=item
                )

        except FoundItem.DoesNotExist:

            pass

    return redirect("dashboard")


# =================================================
# ADD COMMENT
# =================================================

def add_comment(request, item_type, item_id):

    if "user_id" not in request.session:

        return redirect("login")

    if request.method == "POST":

        text = request.POST.get("text")

        if text:

            if item_type == "lost":

                try:

                    item = LostItem.objects.get(id=item_id)

                    Comment.objects.create(
                        user_id=request.session["user_id"],
                        lost_item=item,
                        text=text
                    )

                except LostItem.DoesNotExist:

                    pass

            elif item_type == "found":

                try:

                    item = FoundItem.objects.get(id=item_id)

                    Comment.objects.create(
                        user_id=request.session["user_id"],
                        found_item=item,
                        text=text
                    )

                except FoundItem.DoesNotExist:

                    pass

    return redirect("dashboard")


# =================================================
# SEARCH USERS
# =================================================

def search_users(request):

    if "user_id" not in request.session:

        return redirect("login")

    query = request.GET.get("q", "")

    users = User.objects.exclude(
        id=request.session["user_id"]
    )

    if query:

        users = users.filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, "search_users.html", {
        "users": users,
        "query": query
    })


# =================================================
# SEND CONNECTION REQUEST
# =================================================

def send_connection_request(request, user_id):

    if "user_id" not in request.session:

        return redirect("login")

    sender_id = request.session["user_id"]

    if sender_id == user_id:

        return redirect("search_users")

    try:

        receiver = User.objects.get(id=user_id)

        existing = Connection.objects.filter(
            sender_id=sender_id,
            receiver_id=user_id
        ).first()

        if not existing:

            Connection.objects.create(
                sender_id=sender_id,
                receiver_id=receiver.id,
                status="pending"
            )

            Notification.objects.create(
                user=receiver,
                message=(
                    f"You received a connection request from "
                    f"{request.session.get('user_name', 'a user')}."
                )
            )

    except User.DoesNotExist:

        pass

    return redirect("search_users")


# =================================================
# CONNECTION REQUESTS
# =================================================

def connection_requests(request):

    if "user_id" not in request.session:

        return redirect("login")

    requests = Connection.objects.filter(
        receiver_id=request.session["user_id"],
        status="pending"
    ).order_by("-created_at")

    return render(request, "connection_requests.html", {
        "requests": requests
    })


# =================================================
# ACCEPT CONNECTION
# =================================================

def accept_connection(request, connection_id):

    if "user_id" not in request.session:

        return redirect("login")

    try:

        connection = Connection.objects.get(
            id=connection_id,
            receiver_id=request.session["user_id"],
            status="pending"
        )

        connection.status = "accepted"

        connection.save()

        Notification.objects.create(
            user=connection.sender,
            message=(
                f"{connection.receiver.full_name} "
                f"accepted your connection request."
            )
        )

    except Connection.DoesNotExist:

        pass

    return redirect("connection_requests")


# =================================================
# REJECT CONNECTION
# =================================================

def reject_connection(request, connection_id):

    if "user_id" not in request.session:

        return redirect("login")

    try:

        connection = Connection.objects.get(
            id=connection_id,
            receiver_id=request.session["user_id"],
            status="pending"
        )

        connection.status = "rejected"

        connection.save()

    except Connection.DoesNotExist:

        pass

    return redirect("connection_requests")


# =================================================
# MY CONNECTIONS
# =================================================

def my_connections(request):

    if "user_id" not in request.session:

        return redirect("login")

    user_id = request.session["user_id"]

    connections = Connection.objects.filter(
        Q(sender_id=user_id) | Q(receiver_id=user_id),
        status="accepted"
    ).order_by("-created_at")

    return render(request, "my_connections.html", {
        "connections": connections
    })


# =================================================
# DELETE USER
# =================================================

def delete_user(request, user_id):

    if "user_id" not in request.session:

        return redirect("login")

    if request.session["user_id"] != user_id:

        return redirect("dashboard")

    try:

        user = User.objects.get(id=user_id)

        user.delete()

        request.session.flush()

    except User.DoesNotExist:

        pass

    return redirect("login")


# =================================================
# MY REPORTS
# =================================================

def my_reports(request):

    if "user_id" not in request.session:

        return redirect("login")

    user_id = request.session["user_id"]

    lost_items = LostItem.objects.filter(
        user_id=user_id
    ).order_by("-created_at")

    found_items = FoundItem.objects.filter(
        user_id=user_id
    ).order_by("-created_at")

    return render(request, "my_reports.html", {
        "lost_items": lost_items,
        "found_items": found_items
    })


# =================================================
# MARK LOST ITEM STATUS + NOTIFICATION
# =================================================

def mark_lost_status(request, item_id):

    if "user_id" not in request.session:

        return redirect("login")

    try:

        item = LostItem.objects.get(
            id=item_id,
            user_id=request.session["user_id"]
        )

        status = request.POST.get("status")

        if status in [
            "lost",
            "possible_match",
            "recovered"
        ]:

            old_status = item.status

            item.status = status

            item.save()

            if (
                status == "recovered"
                and old_status != "recovered"
            ):

                Notification.objects.create(

                    user=item.user,

                    message=(
                        f"Your lost item "
                        f"'{item.item_name}' "
                        f"has been marked as Recovered."
                    )
                )

                print("========================================")
                print("LOST ITEM MARKED AS RECOVERED")
                print("ITEM:", item.item_name)
                print("USER:", item.user.email)
                print("RECOVERY NOTIFICATION CREATED")
                print("========================================")

    except LostItem.DoesNotExist:

        pass

    return redirect("my_reports")


# =================================================
# MARK FOUND ITEM STATUS + NOTIFICATION
# =================================================

def mark_found_status(request, item_id):

    if "user_id" not in request.session:

        return redirect("login")

    try:

        item = FoundItem.objects.get(
            id=item_id,
            user_id=request.session["user_id"]
        )

        status = request.POST.get("status")

        if status in [
            "found",
            "returned"
        ]:

            old_status = item.status

            item.status = status

            item.save()

            if (
                status == "returned"
                and old_status != "returned"
            ):

                lost_items = LostItem.objects.filter(
                    category__iexact=item.category
                )

                for lost_item in lost_items:

                    found_name = item.item_name.lower()
                    lost_name = lost_item.item_name.lower()

                    found_location = item.location.lower()
                    lost_location = lost_item.location.lower()

                    if (
                        found_name in lost_name
                        or lost_name in found_name
                        or found_location in lost_location
                        or lost_location in found_location
                    ):

                        Notification.objects.create(

                            user=lost_item.user,

                            message=(
                                f"The found item "
                                f"'{item.item_name}' "
                                f"has been marked as Returned. "
                                f"This may be related to your lost "
                                f"item '{lost_item.item_name}'."
                            )
                        )

                        print("========================================")
                        print("FOUND ITEM MARKED AS RETURNED")
                        print("FOUND ITEM:", item.item_name)
                        print("LOST ITEM:", lost_item.item_name)
                        print("NOTIFICATION CREATED")
                        print(
                            "NOTIFICATION FOR:",
                            lost_item.user.email
                        )
                        print("========================================")

    except FoundItem.DoesNotExist:

        pass

    return redirect("my_reports")


# =================================================
# PROFILE
# =================================================

def profile(request):

    if "user_id" not in request.session:

        return redirect("login")

    try:

        user = User.objects.get(
            id=request.session["user_id"]
        )

    except User.DoesNotExist:

        return redirect("login")

    return render(request, "profile.html", {
        "user": user
    })


# =================================================
# EDIT PROFILE
# =================================================

def edit_profile(request):

    if "user_id" not in request.session:

        return redirect("login")

    try:

        user = User.objects.get(
            id=request.session["user_id"]
        )

    except User.DoesNotExist:

        return redirect("login")

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")

        if User.objects.filter(
            email=email
        ).exclude(
            id=user.id
        ).exists():

            return render(request, "edit_profile.html", {
                "user": user,
                "error": "This email is already registered."
            })

        user.full_name = full_name
        user.email = email
        user.mobile = mobile

        user.save()

        request.session["user_name"] = user.full_name

        return redirect("profile")

    return render(request, "edit_profile.html", {
        "user": user
    })


# =================================================
# FOUNDLINK AI ASSISTANT
# =================================================

def ai_assistant(request):

    if "user_id" not in request.session:

        return redirect("login")

    message = request.POST.get(
        "message",
        ""
    ).strip().lower()

    if not message:

        return render(request, "dashboard.html", {
            "ai_response": (
                "Hi! 👋 I am FoundLink Assistant. "
                "Ask me about reporting items, Smart Match, "
                "notifications, connections, recovery or safety."
            )
        })

    response = ""

    if (
        "lost" in message
        and (
            "report" in message
            or "how" in message
        )
    ):

        response = (
            "To report a lost item, open Report Lost and enter "
            "the item name, category, location, date and description. "
            "You can also upload an image."
        )

    elif (
        "found" in message
        and (
            "report" in message
            or "how" in message
        )
    ):

        response = (
            "To report a found item, open Report Found and enter "
            "the item name, category, location, date and description. "
            "FoundLink will compare the report with existing lost items."
        )

    elif (
        "match" in message
        or "smart" in message
    ):

        response = (
            "FoundLink Smart Match compares a found item with "
            "existing lost-item reports using category, item name, "
            "location and description. A strong possible match "
            "changes the lost item's status to Possible Match and "
            "creates a notification."
        )

    elif "location" in message:

        response = (
            "Location is useful for Smart Matching. If a found item "
            "and a lost item have similar locations, FoundLink can "
            "use that information as an additional matching signal."
        )

    elif "notification" in message:

        response = (
            "Possible Smart Matches appear in your dashboard "
            "notifications. FoundLink can also create notifications "
            "for connection requests and recovery or return updates."
        )

    elif (
        "safe" in message
        or "safety" in message
    ):

        response = (
            "For safety, do not share sensitive personal information "
            "publicly. Use FoundLink's connection features and choose "
            "a safe public place when arranging an item return."
        )

    elif (
        "recover" in message
        or "recovered" in message
        or "return" in message
        or "returned" in message
    ):

        response = (
            "When a lost item is recovered, update its status from "
            "My Reports to Recovered. Found items can be changed "
            "from Found to Returned."
        )

    elif (
        "connection" in message
        or "contact" in message
    ):

        response = (
            "Use Find Users to search for another FoundLink user. "
            "You can send a connection request and manage accepted "
            "connections from My Connections."
        )

    elif (
        "report" in message
        and "item" in message
    ):

        response = (
            "FoundLink has two reporting options: Report Lost for "
            "an item you lost and Report Found for an item you found. "
            "Both reports can include item details and an image."
        )

    elif (
        "dashboard" in message
    ):

        response = (
            "Your dashboard shows recent lost and found reports, "
            "notifications, statistics and your FoundLink activity."
        )

    elif (
        "hello" in message
        or "hi" in message
        or "hey" in message
    ):

        response = (
            "Hello! 👋 I am your FoundLink Assistant. "
            "I can help with lost items, found items, Smart Match, "
            "notifications, connections, recovery and safety."
        )

    else:

        response = (
            "I can help with FoundLink. Try asking:\n\n"
            "• How do I report a lost item?\n"
            "• How do I report a found item?\n"
            "• How does Smart Match work?\n"
            "• Why is location important?\n"
            "• Where can I see notifications?\n"
            "• How do I recover or return an item?\n"
            "• How do I connect with another user?"
        )

    return render(request, "dashboard.html", {
        "ai_response": response
    })


# =================================================
# FOUNDLINK AI CHATBOX
# =================================================

def ai_chat(request):

    # ---------------------------------------------
    # LOGIN CHECK
    # ---------------------------------------------

    if "user_id" not in request.session:

        return JsonResponse({
            "success": False,
            "response": "Please login to use FoundLink Assistant."
        }, status=401)

    # ---------------------------------------------
    # REQUEST CHECK
    # ---------------------------------------------

    if request.method != "POST":

        return JsonResponse({
            "success": False,
            "response": "Invalid request."
        }, status=400)

    # ---------------------------------------------
    # GET MESSAGE
    # ---------------------------------------------

    message = request.POST.get(
        "message",
        ""
    ).strip().lower()

    # ---------------------------------------------
    # EMPTY MESSAGE
    # ---------------------------------------------

    if not message:

        return JsonResponse({
            "success": True,
            "response": (
                "Hi! 👋 I am your FoundLink Assistant. "
                "How can I help you?"
            )
        })

    # ---------------------------------------------
    # DEFAULT ACTIONS
    # ---------------------------------------------

    actions = []

    # ---------------------------------------------
    # LOST ITEM
    # ---------------------------------------------

    if (
        "lost" in message
        and (
            "report" in message
            or "how" in message
        )
    ):

        response = (
            "To report a lost item, open Report Lost. "
            "Enter the item name, category, location, date and "
            "description. You can also upload an image."
        )

        actions = [
            {
                "label": "Report Lost Item",
                "url": reverse("create_lost_item")
            },
            {
                "label": "My Reports",
                "url": reverse("my_reports")
            }
        ]

    # ---------------------------------------------
    # FOUND ITEM
    # ---------------------------------------------

    elif (
        "found" in message
        and (
            "report" in message
            or "how" in message
        )
    ):

        response = (
            "To report a found item, open Report Found and enter "
            "the item name, category, location, date and description. "
            "FoundLink will check it against existing lost-item reports."
        )

        actions = [
            {
                "label": "Report Found Item",
                "url": reverse("create_found_item")
            },
            {
                "label": "View Found Items",
                "url": reverse("view_found_items")
            }
        ]

    # ---------------------------------------------
    # SMART MATCH
    # ---------------------------------------------

    elif (
        "match" in message
        or "smart" in message
    ):

        response = (
            "FoundLink Smart Match compares found items with lost "
            "items using category, item name, location and description. "
            "When a strong possible match is found, the lost item is "
            "marked as Possible Match and the owner receives a notification."
        )

        actions = [
            {
                "label": "Report Found Item",
                "url": reverse("create_found_item")
            },
            {
                "label": "View Lost Items",
                "url": reverse("view_lost_items")
            },
            {
                "label": "View Notifications",
                "url": reverse("dashboard")
            }
        ]

    # ---------------------------------------------
    # LOCATION
    # ---------------------------------------------

    elif "location" in message:

        response = (
            "Location helps FoundLink identify possible matches. "
            "If a found item was reported in a location similar to "
            "where an item was lost, location can provide an additional "
            "matching signal."
        )

        actions = [
            {
                "label": "Report Lost Item",
                "url": reverse("create_lost_item")
            },
            {
                "label": "Report Found Item",
                "url": reverse("create_found_item")
            }
        ]

    # ---------------------------------------------
    # NOTIFICATIONS
    # ---------------------------------------------

    elif "notification" in message:

        response = (
            "Your dashboard contains FoundLink notifications. "
            "Possible Smart Matches, connection requests and some "
            "recovery or return updates can appear there."
        )

        actions = [
            {
                "label": "Open Dashboard",
                "url": reverse("dashboard")
            }
        ]

    # ---------------------------------------------
    # CONNECTIONS / CONTACT
    # ---------------------------------------------

    elif (
        "connection" in message
        or "contact" in message
    ):

        response = (
            "You can search for another FoundLink user from Find Users "
            "and send a connection request. Accepted connections are "
            "available in My Connections."
        )

        actions = [
            {
                "label": "Find Users",
                "url": reverse("search_users")
            },
            {
                "label": "My Connections",
                "url": reverse("my_connections")
            }
        ]

    # ---------------------------------------------
    # RECOVERY / RETURN
    # ---------------------------------------------

    elif (
        "recover" in message
        or "recovered" in message
        or "return" in message
        or "returned" in message
    ):

        response = (
            "After an item is successfully recovered or returned, "
            "update its status from My Reports. Lost items can move "
            "to Recovered, while found items can move to Returned."
        )

        actions = [
            {
                "label": "Open My Reports",
                "url": reverse("my_reports")
            }
        ]

    # ---------------------------------------------
    # SAFETY
    # ---------------------------------------------

    elif (
        "safe" in message
        or "safety" in message
    ):

        response = (
            "For safety, avoid sharing sensitive personal information "
            "publicly. Use FoundLink's connection features and arrange "
            "item returns in a safe public place."
        )

        actions = [
            {
                "label": "Find Users",
                "url": reverse("search_users")
            }
        ]

    # ---------------------------------------------
    # DASHBOARD
    # ---------------------------------------------

    elif "dashboard" in message:

        response = (
            "Your FoundLink dashboard shows recent lost and found "
            "items, notifications, statistics and your activity."
        )

        actions = [
            {
                "label": "Open Dashboard",
                "url": reverse("dashboard")
            }
        ]

    # ---------------------------------------------
    # MY REPORTS
    # ---------------------------------------------

    elif (
        "my report" in message
        or "my reports" in message
    ):

        response = (
            "My Reports shows the lost and found items reported "
            "by your account. You can edit, delete and update "
            "their status there."
        )

        actions = [
            {
                "label": "Open My Reports",
                "url": reverse("my_reports")
            }
        ]

    # ---------------------------------------------
    # LOST / FOUND GENERAL
    # ---------------------------------------------

    elif (
        "lost item" in message
        or "lost item" in message
    ):

        response = (
            "If you lost something, report it using Report Lost. "
            "Add accurate item details, location and date so Smart "
            "Match has useful information."
        )

        actions = [
            {
                "label": "Report Lost Item",
                "url": reverse("create_lost_item")
            }
        ]

    # ---------------------------------------------
    # GREETING
    # ---------------------------------------------

    elif (
        "hello" in message
        or "hi" in message
        or "hey" in message
    ):

        response = (
            "Hello! 👋 I am your FoundLink Assistant. "
            "I can help with reporting items, Smart Match, "
            "notifications, connections, recovery and safety."
        )

        actions = [
            {
                "label": "Report Lost",
                "url": reverse("create_lost_item")
            },
            {
                "label": "Report Found",
                "url": reverse("create_found_item")
            },
            {
                "label": "Open Dashboard",
                "url": reverse("dashboard")
            }
        ]

    # ---------------------------------------------
    # HELP / DEFAULT
    # ---------------------------------------------

    else:

        response = (
            "I can help you with FoundLink. "
            "You can ask me about:\n\n"
            "• Reporting a lost item\n"
            "• Reporting a found item\n"
            "• Smart Match\n"
            "• Notifications\n"
            "• Connections\n"
            "• Recovery and return\n"
            "• Safety"
        )

        actions = [
            {
                "label": "Report Lost",
                "url": reverse("create_lost_item")
            },
            {
                "label": "Report Found",
                "url": reverse("create_found_item")
            },
            {
                "label": "My Reports",
                "url": reverse("my_reports")
            },
            {
                "label": "My Connections",
                "url": reverse("my_connections")
            }
        ]

    # ---------------------------------------------
    # FINAL JSON RESPONSE
    # ---------------------------------------------

    return JsonResponse({
        "success": True,
        "response": response,
        "actions": actions
    })

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Authentication
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),

    # Forgot Password
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("reset-password/", views.reset_password, name="reset_password"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("delete-notification/<int:notification_id>/", views.delete_notification, name="delete_notification"),

    # AI Assistant
    path("ai-assistant/", views.ai_assistant, name="ai_assistant"),
    path("ai-chat/", views.ai_chat, name="ai_chat"),
    path("ai-lost-item-finder/", views.ai_lost_item_finder, name="ai_lost_item_finder"),

    # Lost Items
    path("create-lost-item/", views.create_lost_item, name="create_lost_item"),
    path("view-lost-items/", views.view_lost_items, name="view_lost_items"),
    path("edit-lost-item/<int:item_id>/", views.edit_lost_item, name="edit_lost_item"),
    path("delete-lost-item/<int:item_id>/", views.delete_lost_item, name="delete_lost_item"),

    # Found Items
    path("create-found-item/", views.create_found_item, name="create_found_item"),
    path("view-found-items/", views.view_found_items, name="view_found_items"),
    path("edit-found-item/<int:item_id>/", views.edit_found_item, name="edit_found_item"),
    path("delete-found-item/<int:item_id>/", views.delete_found_item, name="delete_found_item"),

    # Likes
    path("like/<str:item_type>/<int:item_id>/", views.like_post, name="like_post"),

    # Comments
    path("comment/<str:item_type>/<int:item_id>/", views.add_comment, name="add_comment"),

    # Users
    path("search-users/", views.search_users, name="search_users"),
    path("delete-user/<int:user_id>/", views.delete_user, name="delete_user"),

    # Connections
    path("send-connection-request/<int:user_id>/", views.send_connection_request, name="send_connection_request"),
    path("connection-requests/", views.connection_requests, name="connection_requests"),
    path("accept-connection/<int:connection_id>/", views.accept_connection, name="accept_connection"),
    path("reject-connection/<int:connection_id>/", views.reject_connection, name="reject_connection"),
    path("my-connections/", views.my_connections, name="my_connections"),

    # My Reports
    path("my-reports/", views.my_reports, name="my_reports"),

    # Item Status
    path("mark-lost-status/<int:item_id>/", views.mark_lost_status, name="mark_lost_status"),
    path("mark-found-status/<int:item_id>/", views.mark_found_status, name="mark_found_status"),

    # Profile
    path("profile/", views.profile, name="profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
]

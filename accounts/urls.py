from django.urls import path
from . import views


urlpatterns = [

    # =================================================
    # HOME
    # =================================================

    path(
        "",
        views.home,
        name="home"
    ),


    # =================================================
    # AUTHENTICATION
    # =================================================

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        views.login,
        name="login"
    ),

    path(
        "logout/",
        views.logout,
        name="logout"
    ),


    # =================================================
    # FORGOT PASSWORD
    # =================================================

    path(
        "forgot-password/",
        views.forgot_password,
        name="forgot_password"
    ),

    path(
        "verify-otp/",
        views.verify_otp,
        name="verify_otp"
    ),

    path(
        "reset-password/",
        views.reset_password,
        name="reset_password"
    ),


    # =================================================
    # DASHBOARD
    # =================================================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "delete-notification/<int:notification_id>/",
        views.delete_notification,
        name="delete_notification"
    ),


    # =================================================
    # AI ASSISTANT
    # =================================================

    path(
        "ai-assistant/",
        views.ai_assistant,
        name="ai_assistant"
    ),

    path(
        "ai-chat/",
        views.ai_chat,
        name="ai_chat"
    ),


    # =================================================
    # LOST ITEMS
    # =================================================

    path(
        "create-lost-item/",
        views.create_lost_item,
        name="create_lost_item"
    ),

    path(
        "view-lost-items/",
        views.view_lost_items,
        name="view_lost_items"
    ),

    path(
        "edit-lost-item/<int:item_id>/",
        views.edit_lost_item,
        name="edit_lost_item"
    ),

    path(
        "delete-lost-item/<int:item_id>/",
        views.delete_lost_item,
        name="delete_lost_item"
    ),


    # =================================================
    # FOUND ITEMS
    # =================================================

    path(
        "create-found-item/",
        views.create_found_item,
        name="create_found_item"
    ),

    path(
        "view-found-items/",
        views.view_found_items,
        name="view_found_items"
    ),

    path(
        "edit-found-item/<int:item_id>/",
        views.edit_found_item,
        name="edit_found_item"
    ),

    path(
        "delete-found-item/<int:item_id>/",
        views.delete_found_item,
        name="delete_found_item"
    ),


    # =================================================
    # LIKE / UNLIKE
    # =================================================

    path(
        "like/<str:item_type>/<int:item_id>/",
        views.like_post,
        name="like_post"
    ),


    # =================================================
    # COMMENTS
    # =================================================

    path(
        "comment/<str:item_type>/<int:item_id>/",
        views.add_comment,
        name="add_comment"
    ),


    # =================================================
    # SEARCH USERS
    # =================================================

    path(
        "search-users/",
        views.search_users,
        name="search_users"
    ),


    # =================================================
    # DELETE USER
    # =================================================

    path(
        "delete-user/<int:user_id>/",
        views.delete_user,
        name="delete_user"
    ),


    # =================================================
    # CONNECTIONS
    # =================================================

    path(
        "send-connection-request/<int:user_id>/",
        views.send_connection_request,
        name="send_connection_request"
    ),

    path(
        "connection-requests/",
        views.connection_requests,
        name="connection_requests"
    ),

    path(
        "accept-connection/<int:connection_id>/",
        views.accept_connection,
        name="accept_connection"
    ),

    path(
        "reject-connection/<int:connection_id>/",
        views.reject_connection,
        name="reject_connection"
    ),

    path(
        "my-connections/",
        views.my_connections,
        name="my_connections"
    ),


    # =================================================
    # MY REPORTS
    # =================================================

    path(
        "my-reports/",
        views.my_reports,
        name="my_reports"
    ),


    # =================================================
    # ITEM STATUS
    # =================================================

    path(
        "mark-lost-status/<int:item_id>/",
        views.mark_lost_status,
        name="mark_lost_status"
    ),

    path(
        "mark-found-status/<int:item_id>/",
        views.mark_found_status,
        name="mark_found_status"
    ),


    # =================================================
    # PROFILE
    # =================================================

    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    path(
        "edit-profile/",
        views.edit_profile,
        name="edit_profile"
    ),

]
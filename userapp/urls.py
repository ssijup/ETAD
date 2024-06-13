from django.urls import path

from .import views


urlpatterns = [


    path("guntest", views.guntest, name="guntest"),

    path("match_users/<int:primary_user_id>", views.match_users, name="match_users"),

    path("user_signup", views.user_signup, name="user_signup"),
    path("", views.user_login, name="user_login"),
    path("user_logout", views.user_logout, name="user_logout"),


    path("user_dashboard", views.user_dashboard, name="user_dashboard"),


    path("user_signup_details_tellus1", views.user_signup_details_tellus1, name="user_signup_details_tellus1"),
    path("user_signup_details_tellus2", views.user_signup_details_tellus2, name="user_signup_details_tellus2"),
    path("user_signup_details_likes", views.user_signup_details_likes, name="user_signup_details_likes"),


    path("create_user_post", views.create_user_post, name="create_user_post"),
    path("user_liking_the_post/", views.user_liking_the_post, name="user_liking_the_post"),


    path("user_accecpting_match_request", views.user_accecpting_match_request, name="user_accecpting_match_request"),
    path("user_list_for_chat", views.user_list_for_chat, name="user_list_for_chat"),


    path("user_chat_room", views.user_chat_room, name="user_chat_room"),
    path("like_user_profiles", views.like_user_profiles, name="like_user_profiles"),
    path("user_disliking_profiles", views.user_disliking_profiles, name="user_disliking_profiles"),

    
    path("upload_profileimage", views.upload_profileimage, name="upload_profileimage"),
    path("edit_user_interests", views.edit_user_interests, name="edit_user_interests"),

    path("user_matching_profiles", views.user_matching_profiles, name="user_matching_profiles"),

]
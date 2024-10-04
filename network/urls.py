
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("profile/<int:profile_id>/", views.profile, name="profile"),
    path("follow/<int:profile_id>/", views.follow, name="follow"),
    path("unfollow/<int:profile_id>/", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),

    #api route
    path("edit", views.edit, name="edit"),
    path('like/<int:post_id>', views.like_post, name='like_post'),
    path('unlike/<int:post_id>', views.unlike_post, name='unlike_post'),
]

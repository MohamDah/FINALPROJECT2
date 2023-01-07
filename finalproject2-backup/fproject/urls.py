from django.urls import path
from fproject import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("explore", views.explore, name="explore"),
    path("send_request", views.send_request, name="send_request"),
    path("notifications", views.notifications, name="notifications"),
    path("friends", views.friends, name="friends"),
    path("chat/<str:username>", views.chat, name="chat"),
    path("send_message", views.send_message, name="send_message"),
    path("json_chat/<str:username>", views.json_chat, name="json_chat")
]

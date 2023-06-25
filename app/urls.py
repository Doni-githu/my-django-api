from . import views
from django.urls import path

urlpatterns = [
    path("login/", views.login),
    path("signup/", views.signup),
    path("user/", views.getUser),
]

from django.urls import path

from .views import logout, sign_in, sign_up

urlpatterns = [
    path(
        route="sign-up/",
        view=sign_up,
        name="sign_up",
    ),
    path(
        route="sign-in/",
        view=sign_in,
        name="sign_in",
    ),
    path(
        route="logout/",
        view=logout,
        name="logout",
    ),
]

from django.urls import path
from .views import get_wallet_balance

urlpatterns = [
    path(
        route="balance/get",
        view= get_wallet_balance,
        name="get_balance",
    ),
    # path(
    #     route="sign-in/",
    #     view=sign_in,
    #     name="sign_in",
    # )
]

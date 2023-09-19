from django.db import models

from extentions import BaseModel


class Wallet(BaseModel):
    balance = models.IntegerField(default=0)
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "wallets"

    def check_wallet_solvency(self, cashflow: int) -> bool:
        return (self.balance - cashflow) >= 0

from django.db import models
from extentions import BaseModel, enums


class Transaction(BaseModel):
    amount = models.IntegerField()
    status = models.CharField(default=enums.TransactionStatusEnum.successful.value, max_length=35)
    type = models.CharField(max_length=6)
    category = models.ForeignKey(
        "transactions.UserCategory",
        on_delete=models.SET_NULL,
        db_column="category_id",
        related_name="transection_for_categories",
        null=True,
    )

    class Meta:
        db_table = 'transactions'


class UserTransaction(BaseModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="user_transaction_for_users",
    )
    transaction = models.ForeignKey(
        "transactions.Transaction",
        on_delete=models.CASCADE,
        db_column="transaction_id",
        related_name="user_transaction_for_transaction",
    )

    class Meta:
        db_table = "user_transactions"


class UserCategory(BaseModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="user_category_for_users",
    )
    title = models.CharField(max_length=100)

    class Meta:
        db_table = 'user_categories'

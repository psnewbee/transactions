from django.urls import path

from .views import (
    create_transaction,
    create_transaction_category,
    delete_transaction,
    delete_transaction_categories,
    get_transaction_categories,
    get_transactions,
    update_transaction,
    update_transaction_category,
)

urlpatterns = [
    path(
        route="category/all",
        view=get_transaction_categories,
        name="get_transaction_categories",
    ),
    path(
        route="category/create",
        view=create_transaction_category,
        name="create_transaction_category",
    ),
    path(
        route="category/<int:transaction_category_id>/update",
        view=update_transaction_category,
        name="update_transaction_category",
    ),
    path(
        route="category/<int:transaction_category_id>/delete",
        view=delete_transaction_categories,
        name="delete_transaction_category",
    ),
    path(
        route="all",
        view=get_transactions,
        name="get_transactions",
    ),
    path(
        route="add",
        view=create_transaction,
        name="create_transaction",
    ),
    path(
        route="<int:transaction_id>/update",
        view=update_transaction,
        name="update_transaction",
    ),
    path(
        route="<int:transaction_id>/delete",
        view=delete_transaction,
        name="delete_transaction",
    ),
]

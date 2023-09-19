from django.contrib.auth import models as auth_models
from django.contrib.auth import validators
from django.db import models

from extentions import BaseModel, UserManager


class User(auth_models.AbstractBaseUser, BaseModel):
    email = models.EmailField(
        max_length=50,
        unique=True,
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )

    objects: "UserManager" = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @classmethod
    def normalize_email(cls, email: str) -> str:
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name + "@" + domain_part.lower()
        return email

    class Meta:
        db_table = "users"

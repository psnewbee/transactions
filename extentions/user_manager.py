from typing import Any, TYPE_CHECKING
from django.apps import apps
from django.contrib.auth import hashers, models, password_validation
from django.core.exceptions import ValidationError, BadRequest

if TYPE_CHECKING:
    from apps.users.models import User


class UserManager(models.UserManager):

    def _create_user(self,
                     email: str, 
                     password: str, 
                     **extra_fields: Any) -> 'User':
        if not email:
            raise ValueError("The given email must be set")
        GlobalUserModel = apps.get_model("users", "User")
        GlobalUserModel.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields)
        
        try:
            password_validation.validate_password(password)
        except ValidationError as e:
            raise BadRequest(detail=e.__dict__["error_list"][0])
        
        user.password = hashers.make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str,  password: str = None, **extra_fields: Any) -> 'User':
        return self._create_user(email=email, password=password, **extra_fields)


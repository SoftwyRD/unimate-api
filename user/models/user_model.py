from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from college.models import CollegeModel

from ..managers import UserManager


class UserModel(AbstractUser):
    id = models.AutoField(
        _("id"),
        help_text=_("Autogenerated (non editable) user id"),
        primary_key=True,
        unique=True,
        editable=False,
    )
    first_name = models.CharField(
        _("first name"),
        help_text=_("User legal first name"),
        max_length=50,
    )
    last_name = models.CharField(
        _("last name"),
        help_text=_("User legal last name"),
        max_length=50,
    )
    username = models.CharField(
        _("username"),
        help_text=_("User username"),
        unique=True,
        max_length=20,
        validators=(AbstractUser.username_validator,),
        error_messages={
            "unique": _("A user with that username already exists"),
        },
    )
    email = models.EmailField(
        _("email"),
        help_text=_("User email"),
        unique=True,
        max_length=255,
        error_messages={
            "unique": _("A user with that email already exists"),
        },
    )
    password = models.CharField(
        _("password"),
        help_text=_("User hashed password"),
        max_length=128,
    )
    college = models.ForeignKey(
        verbose_name=_("college"),
        help_text=_("College"),
        to=CollegeModel,
        on_delete=models.CASCADE,
        related_name="students",
        null=True,
        blank=True,
    )
    verified = models.BooleanField(
        _("verified"), help_text=_("Is user verified"), default=False
    )

    objects = UserManager()

    REQUIRED_FIELDS = ("first_name", "last_name", "email")

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "user"

    def __str__(self):
        return self.username

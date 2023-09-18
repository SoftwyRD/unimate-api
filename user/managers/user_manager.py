from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create(self, **kwargs):
        password = kwargs.pop("password")
        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create(**kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        case_insensitive_username_field = "{}__iexact".format(
            self.model.USERNAME_FIELD
        )
        return self.get(**{case_insensitive_username_field: username})

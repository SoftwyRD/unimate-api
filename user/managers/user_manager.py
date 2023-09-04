from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create(
        self,
        first_name,
        last_name,
        username,
        email,
        password,
    ):
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        first_name,
        last_name,
        username,
        email,
        password,
    ):
        user = self.create(
            first_name,
            last_name,
            username,
            email,
            password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        case_insensitive_username_field = "{}__iexact".format(
            self.model.USERNAME_FIELD
        )
        return self.get(**{case_insensitive_username_field: username})

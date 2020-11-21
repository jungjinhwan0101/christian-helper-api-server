from django.contrib.auth.base_user import BaseUserManager


class ORMUserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

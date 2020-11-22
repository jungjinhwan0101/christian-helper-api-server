from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

from user.models.managers import ORMUserManager
from user.token import AccessToken


class UserAccessToken:
    def __init__(self, user):
        self.user = user

    @property
    def payload(self):
        return {
            'id': self.user.id,
            'username': self.user.username
        }

    def obtain_token(self):
        return AccessToken.encrypt(self.payload)


class ORMUser(AbstractBaseUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    USERNAME_FIELD = 'username'
    objects = ORMUserManager()

    @property
    def access_token(self):
        return UserAccessToken(self)

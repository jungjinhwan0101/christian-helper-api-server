from abc import ABC

from base.exceptions import ValidationError
from user.domain.services import user_service


class Command(ABC):
    def execute(self, data):
        raise NotImplementedError()


def get_data(data, field_name, require=True):
    value = data.get(field_name, None)
    if require and not value:
        raise ValidationError(f'{field_name} 은 필수 입력값 입니다.')
    return value


class UserJoinCommand(Command):
    def execute(self, data):
        username = get_data(data, 'username')
        password = get_data(data, 'password')
        user = user_service.create_user(username=username, password=password)
        return True, user


class UserLoginCommand(Command):
    def execute(self, data):
        username = get_data(data, 'username')
        password = get_data(data, 'password')

        user = user_service.find_by_username(username)
        if not user.check_password(password):
            raise ValidationError('패스워드가 일치하지 않습니다.')
        result = {
            'user': user,
            'access_token': user.access_token.obtain_token()
        }
        return True, result

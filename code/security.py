from werkzeug.security import safe_str_cmp
from models.user import UserModels


def authenticate(username, password):
    print("username: " + username + ", " + "password: " + password)
    user = UserModels.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    print("payload: ", payload)
    user_id = payload['identity']
    return UserModels.find_by_id(user_id)
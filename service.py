import repository
from models import User
import utils


def create_user(user: User):
    user.password = utils.hash_string(user.password)
    return repository.create_user(user)


def get_user(username, password):
    password = utils.hash_string(password)
    user = repository.get_user(username, password)
    if user is None:
        return None, "Incorrect username or password"
    return user.id, None

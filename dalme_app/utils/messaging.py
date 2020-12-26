from django.contrib.auth.models import User
from async_messages import message_user
from django.contrib.messages import constants
from django_q.tasks import AsyncTask
from django_currentuser.middleware import get_current_user


def send_message(instance, user=None, level=None):
    if isinstance(instance, AsyncTask):
        message = instance.result['message']
        level = instance.result['level']
        user = User.objects.get(id=instance.result['user_id'])
    elif type(instance) is dict:
        message = instance['message']
        level = instance['level']
        user = User.objects.get(id=instance['user_id'])
    else:
        try:
            message = instance
            level = constants.INFO
            user = get_current_user()
        except Exception as e:
            message = f'There was an error while trying to message you: {str(e)}'
            level = constants.WARNING
            user = get_current_user()

    if message and user and level:
        message_user(user, message, level)

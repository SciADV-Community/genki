from django.contrib.auth.backends import BaseBackend
from playthrough.models import User


class DiscordAuthenticationBackend(BaseBackend):
    def authenticate(self, request, user_info):
        username = f"{user_info['username']}#{user_info['discriminator']}"
        try:
            user = User.objects.get(id=str(user_info['id']))
            print(f'found user: {user}')
            user.username = username
            user.save()
        except User.DoesNotExist:
            # Create a new user
            user = User(id=str(user_info['id']), username=username)
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

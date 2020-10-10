from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from playthrough.models import Archive, User
from playthrough.utils import get_users_in_archive


@receiver(post_save, sender=Archive)
def index_users(sender, instance: Archive, **kwargs):
    """Index the users present in a certain archive.

    :param sender: The `django.db.models.Model` class sending the signal.
    :param instance: The `playthrough.models.Archive` being saved.
    """
    user_ids = get_users_in_archive(instance)
    users = [User.objects.get_or_create(id=user_id)[0] for user_id in user_ids]
    instance.users.add(*users)


@receiver(pre_delete, sender=Archive)
def cleanup_archives(sender, instance: Archive, **kwargs):
    """Delete the archive files when the model gets deleted.

    :param sender: The `django.db.models.Model` class sending the signal.
    :param instance: The `playthrough.models.Archive` being saved.
    """
    instance.users.clear()
    instance.file.delete(save=False)

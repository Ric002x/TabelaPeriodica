import os

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from learn_lab.models import Activity


def delete_file(instance):
    try:
        os.remove(instance.file.path)
    except (ValueError, FileNotFoundError, AttributeError):
        ...


@receiver(pre_delete, sender=Activity)
def delete_old_file(signal, instance, *args, **kwargs):
    old_instance = Activity.objects.filter(pk=instance.id).first()

    if old_instance:
        delete_file(old_instance)


@receiver(pre_save, sender=Activity)
def update_activity_file(signal, instance, *args, **kwargs):
    old_instance = Activity.objects.filter(pk=instance.id).first()
    is_new_instance = old_instance != instance.file

    if not old_instance:
        return

    if is_new_instance:
        delete_file(old_instance)

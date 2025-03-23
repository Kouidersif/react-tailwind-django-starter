from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from accounts.models import UserProfile
import os


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        
        


@receiver(post_delete, sender=UserProfile)
def auto_delete_file_on_delete(sender, instance: UserProfile, **kwargs: dict):
    """
    Deletes file from filesystem
    when corresponding `UserProfile` object is deleted.
    """
    if instance.profile_picture:
        try:
            if os.path.isfile(instance.profile_picture.path):
                os.remove(instance.profile_picture.path)
        except Exception as e:
            print(e)
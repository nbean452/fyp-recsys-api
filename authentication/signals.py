from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from base.models import UserDetail


@receiver(post_save, sender=User)
def create_detail(sender, instance, created, **kwargs):
    if created:
        UserDetail.objects.create(user=instance)

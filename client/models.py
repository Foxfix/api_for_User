from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from decimal import Decimal


class User(AbstractUser):
    """User with app settings.""" 
    SHIRT_SIZES = (
        ('Close', 'Close'),
        ('Open', 'Open'),
    )
    balance = models.DecimalField(max_digits=20,decimal_places=4,default=Decimal('0.0000'))
    passport_number = models.CharField(max_length=15, default="000000")
    accaunt = models.CharField(max_length=10, choices=SHIRT_SIZES, default='Open')


@receiver(pre_save, sender=User)
def set_new_user_inactive(sender, instance, **kwargs):
    """
    Make a client's account in inactive state after registration.
    """
    if not instance.is_superuser:
        if instance._state.adding is True:
            instance.is_active = False
        else:
            print("Updating User Record")


   
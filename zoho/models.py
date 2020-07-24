from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class tokenmanager(models.Model):
	access_token = models.CharField(max_length=50)
	refresh_token = models.CharField(max_length=50)
	api_domain = models.CharField(max_length=10)
	token_type = models.CharField(max_length=20)
	expires_in = models.DateTimeField(max_length=20)
	
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	mob = models.IntegerField(blank=True,null=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

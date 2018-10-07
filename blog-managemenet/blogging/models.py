# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    date_added = models.DateField(auto_now_add=True, blank=True)

    followed = models.ManyToManyField("self", symmetrical=False)



    def __unicode__(self):
    	return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(pre_delete, sender=User)
def remove_follower(sender, instance, *args, **kwargs):

    for every_profile in Profile.objects.all():
        every_profile.followed.remove(instance.profile)



class Blog(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField(max_length=500)


    def __unicode__(self):
        return self.title


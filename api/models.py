# -*- coding: utf-8 -*-

import datetime

from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver


class Company(models.Model):
    company_name = models.CharField(max_length=16,default="Train Rabbits")

    def __str__(self):
        return str(self.company_name)


# User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_company_manager = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = self.user.username

    def __str__(self):
        return str(self.user)


'''
# service functions
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# do not touch!
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
'''


# objects
class Game(models.Model):
    title = models.CharField(max_length=16)

    def __str__(self):
        return str(self.title)


# objects store information about every game played
class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date = models.DateTimeField('date played', default=timezone.now)

    def played_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return ' '.join([str(self.game), str(self.user), str(self.score)])

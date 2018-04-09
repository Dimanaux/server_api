from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Game(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return str(self.title)


class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return ' '.join(str(self.game) + str(self.user) + str(self.score))

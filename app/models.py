from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=32)
    dtm = models.DateTimeField()
    lat = models.DecimalField(max_digits=10, decimal_places=8)
    lon = models.DecimalField(max_digits=11, decimal_places=8)
    address = models.CharField(max_length=128)
    creator = models.ForeignKey(User)
    description = models.TextField()
    image = models.ImageField()
    key = models.CharField(max_length=16, unique=True)
    deadline = models.DateTimeField()
    budget = models.DecimalField(max_digits=9, decimal_places=2)
    collected_money = models.DecimalField(max_digits=9, decimal_places=2)


class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    key = models.CharField(max_length=16, unique=True)
    recipient = models.CharField(max_length=32)
    count = models.SmallIntegerField(default=1)


class Hit(models.Model):
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE)
    dtm = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=256)
    referal = models.URLField(null=True)
    ip = models.GenericIPAddressField()


class Decision(models.Model):
    event = models.ForeignKey(Invitation, on_delete=models.CASCADE)
    dtm = models.DateTimeField(auto_now_add=True)
    decision = models.BooleanField()
    is_valid = models.BooleanField(default=True)



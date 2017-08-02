from django.db import models


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=30)
    date_of_start = models.DateField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=30)
    contact = models.ForeignKey('Person', on_delete=models.DO_NOTHING)
    description = models.TextField()
    image = models.ImageField()
    creator = models.CharField(max_length=30)
    url = models.URLField()
    deadline_confirm = models.DateField()
    budget = models.DecimalField(max_digits=9, decimal_places=2)
    collected_money = models.DecimalField(max_digits=9, decimal_places=2)
    deadline_change_decision = models.DateField()


class Invite(models.Model):
    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
    )
    url = models.URLField()
    receiver = models.CharField(max_length=30)
    count = models.SmallIntegerField(default=1)


class LogInInvite(models.Model):
    invite = models.OneToOneField('Invite')
    date_logged = models.DateField()
    user_agent = models.CharField(max_length=30)
    ip = models.GenericIPAddressField()


class Solution(models.Model):
    invite = models.OneToOneField('Invite')
    date = models.DateField()
    decision = models.BooleanField()
    actuality = models.BooleanField()


class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    link = models.URLField("Contact info (email or VK)", max_length=30)



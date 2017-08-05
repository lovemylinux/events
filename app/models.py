from django.contrib.auth.models import User
from django.db import models
from django.utils.deconstruct import deconstructible
import uuid, os


@deconstructible
class UploadToPathAndRename(object):
    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=32)
    dtm = models.DateTimeField()
    lat = models.DecimalField(max_digits=10, decimal_places=8)
    lon = models.DecimalField(max_digits=11, decimal_places=8)
    address = models.CharField(max_length=128)
    creator = models.ForeignKey(User)
    description = models.TextField()
    image = models.ImageField(upload_to=UploadToPathAndRename('app/static/images'))
    key = models.CharField(max_length=36, unique=True)
    deadline = models.DateTimeField()
    budget = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    collected_money = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return 'Event({}, {})'.format(self.id, self.name)

    def __repr__(self):
        return 'Event({}, {})'.format(self.id, self.name)


class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    key = models.CharField(max_length=36, unique=True)
    recipient = models.CharField(max_length=32)
    count = models.SmallIntegerField(default=1)

    def __str__(self):
        return 'Invitation({}, {})'.format(self.id, self.recipient)

    def __repr__(self):
        return 'Invitation({}, {})'.format(self.id, self.recipient)


class Hit(models.Model):
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE)
    dtm = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=256)
    referal = models.URLField(null=True)
    ip = models.GenericIPAddressField()

    def __str__(self):
        return 'Hit({}, {})'.format(self.id, self.name)

    def __repr__(self):
        return 'Hit({}, {})'.format(self.id, self.name)


class Decision(models.Model):
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE)
    dtm = models.DateTimeField(auto_now_add=True)
    decision = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return 'Decision({}, {})'.format(self.id, self.decision)

    def __repr__(self):
        return 'Decision({}, {})'.format(self.id, self.decision)




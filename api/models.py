from django.conf import settings

try:
    from local_settings import *
except ImportError:
    pass

settings.configure(DATABASE_ENGINE=DATABASE_ENGINE, DATABASE_NAME=DATABASE_NAME, DATABASE_USER=DATABASE_USER, DATABASE_PASSWORD=DATABASE_PASSWORD)

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    is_men = models.BooleanField()

    class Meta:
        db_table = 'user'


class Quote(models.Model):
    quote = models.CharField(max_length=140, unique=True)

    class Meta:
        db_table = 'quote'

    def __unicode__(self):
        return self.quote

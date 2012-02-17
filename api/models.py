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
    name = models.CharField(max_length=15,blank=True)
    patronymic = models.CharField(max_length=15, blank=True)
    birthday = models.DateField(null=True)
    birthplace = models.CharField(max_length=15, blank=True)
    liveplace = models.CharField(max_length=15, blank=True)
    phone = models.IntegerField(max_length=15, null=True)
    skype = models.CharField(max_length=15, blank=True)
    vkontakte = models.URLField(max_length=15, blank=True)
    facebook = models.URLField(max_length=15, blank=True)
    twitter = models.URLField(max_length=15, blank=True)
    site = models.URLField(max_length=15, blank=True)
    work = models.CharField(max_length=15, blank=True)
    school = models.CharField(max_length=15, blank=True)
    institute = models.CharField(max_length=15, blank=True)
    about = models.TextField(max_length=300, blank=True)

    class Meta:
        db_table = 'user'

class Quote(models.Model):
    quote = models.CharField(max_length=140, unique=True)

    class Meta:
        db_table = 'quote'

    def __unicode__(self):
        return self.quote

class Anekdote(models.Model):
    anek = models.TextField()

    class Meta:
        db_table = 'anekdots'

    def __unicode__(self):
        return self.anek

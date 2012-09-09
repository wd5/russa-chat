import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'local_settings'

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    is_men = models.BooleanField()
    name = models.CharField(max_length=15,blank=True)
    surname = models.CharField(max_length=15,blank=True)
    patronymic = models.CharField(max_length=15, blank=True)
    birthday = models.DateField(null=True)
    birthplace = models.CharField(max_length=30, blank=True)
    liveplace = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    skype = models.CharField(max_length=32, blank=True)
    vkontakte = models.URLField(max_length=50, blank=True)
    facebook = models.URLField(max_length=50, blank=True)
    twitter = models.URLField(max_length=50, blank=True)
    site = models.URLField(max_length=100, blank=True)
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

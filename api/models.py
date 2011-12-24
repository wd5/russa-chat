from django.conf import settings

settings.configure(DATABASE_ENGINE='django.db.backends.mysql', DATABASE_NAME='chat', DATABASE_USER='chat', DATABASE_PASSWORD='kjasdlkj7askjhdg')

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    is_men = models.BooleanField()

    class Meta:
        db_table = 'user'
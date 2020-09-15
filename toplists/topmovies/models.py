from django.db import models
from django.conf import settings
from django.db.models import JSONField

class MovieList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie_list = JSONField()
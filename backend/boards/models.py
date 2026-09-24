from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class Board(models.Model):
    title = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    members = models.ManyToManyField(User, related_name='boards', blank=True)

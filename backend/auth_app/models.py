from django.db import models
from django.contrib.auth.models import User

"""
Represent additional profile informations
"""


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"

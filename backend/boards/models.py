from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class Board(models.Model):
    title = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    members = models.ManyToManyField(User, related_name='boards', blank=True)


class Task(models.Model):

    title = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    description = models.CharField(
        max_length=350, validators=[MinLengthValidator(3)])

    class Status(models.TextChoices):
        TODO = 'to-do', 'To Do'
        IN_PROGRESS = 'in-progress', 'In Progress'
        REVIEW = 'review', 'Review'
        DONE = 'done', 'Done'

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='task_assignees', blank=True, null=True)
    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='task_reviewers', blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

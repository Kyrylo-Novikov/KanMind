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

    status = models.CharField(max_length=20, choices=Status, default='to-do')

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    prio = models.CharField(max_length=20, choices=Priority, default='medium')

    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='task_assignees', blank=True, null=True)
    board = models.ForeignKey(
        'Board', on_delete=models.CASCADE, related_name='tasks')
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='task_reviewers', blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)


class Comment(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments_author', blank=True, null=True)
    content = models.TextField(
        max_length=350, validators=[MinLengthValidator(3)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username}on Task {self.task_id}"

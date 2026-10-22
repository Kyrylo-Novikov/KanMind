from django.contrib import admin
from .models import Task, Board, Comment


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Board model.
    """
    list_display = ('id', 'title', 'owner', 'get_members_count')
    list_display_links = ('id', 'title')
    list_filter = ('owner',)
    search_fields = ('title', 'owner__username')

    def get_members_count(self, obj) -> int:
        """
        Counts the members on the board.
        """
        return obj.members.count()


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Task model
    """
    list_display = ('id', 'board', 'title', 'description', 'status', 'priority',
                    'assignee', 'reviewer', 'due_date', 'comments_count',)
    list_display_links = ('id', 'title', 'board')
    list_filter = ('status', 'priority')

    def comments_count(self, obj) -> int:
        """
        Counts the comments on the task.
        """
        return obj.comments.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Comment model
    """
    list_display = ('id', 'created_at', 'author', 'content')
    list_display_links = ('id', 'author')
    list_filter = ('author',)

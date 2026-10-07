from rest_framework import serializers
from django.contrib.auth.models import User
from board_app.models import Board, Task, Comment


class MemberSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='username', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'last_login',
                  'date_joined', 'user_permissions']


class TaskReadSerializer(serializers.ModelSerializer):
    assignee = MemberSerializer()
    reviewer = MemberSerializer()
    priority = serializers.CharField(source='prio')
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj) -> int:
        count = obj.comments.count()
        print("Anzahl der Kommentare für den task", obj.id, count)
        return count

    class Meta:
        model = Task
        fields = ['id', 'title', 'due_date', 'reviewer', 'board',
                  'assignee', 'priority', 'status', 'description', 'comments_count']


class TaskCreatUpdateSerializer(serializers.ModelSerializer):
    priority = serializers.CharField(source='prio', required=False)
    assignee_id = serializers.PrimaryKeyRelatedField(source="assignee", allow_null=True,
                                                     queryset=User.objects.all(), required=False)
    reviewer_id = serializers.PrimaryKeyRelatedField(source="reviewer",
                                                     queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'due_date', 'reviewer_id', 'board',
                  'assignee_id', 'priority', 'status', 'description']
        read_only_fields = ['id']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.assignee:
            rep['assignee'] = MemberSerializer(instance.assignee).data
        if instance.reviewer:
            rep['reviewer'] = MemberSerializer(instance.reviewer).data
        return rep


class BoardSerializer(serializers.ModelSerializer):
    tasks = TaskReadSerializer(many=True, read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    title = serializers.CharField(max_length=50)

    def get_member_count(self, obj) -> int:
        return obj.members.count()

    def get_ticket_count(self, obj) -> int:
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj) -> int:
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj) -> int:
        return obj.tasks.filter(prio='high').count()

    class Meta:
        model = Board
        fields = ['id', 'tasks', 'members', 'member_count', 'ticket_count',
                  'tasks_to_do_count', 'tasks_high_prio_count', 'title']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['members'] = MemberSerializer(
            instance.members.all(), many=True).data

        return rep


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'task', 'created_at']

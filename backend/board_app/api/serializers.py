from datetime import date
from django.contrib.auth.models import User
from rest_framework import serializers
from board_app.models import Board, Task, Comment


def validate_board_member(serializer, user):
    """
    Validate whether the user is a member of the board
    """
    if not user:
        return user
    board = None
    if serializer.instance and hasattr(serializer.instance, 'board'):
        board = serializer.instance.board
    elif 'board' in serializer.initial_data:
        board = Board.objects.filter(
            id=serializer.initial_data.get('board')).first()
    if board and not board.members.filter(id=user.id).exists():
        raise serializers.ValidationError(
            "Given User is not a  member of this board")
    return user


class MemberSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='username', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email']


class TaskReadCreateSerializer(serializers.ModelSerializer):
    assignee = MemberSerializer()
    reviewer = MemberSerializer()
    priority = serializers.CharField()
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj) -> int:
        count = obj.comments.count()
        return count

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority',
                  'assignee', 'reviewer', 'due_date', 'comments_count']

        def validate_assignee(self, value):
            return validate_board_member(self, value)

        def validate_reviewer(self, value):
            return validate_board_member(self, value)


class TaskUpdateDeleteSerializer(serializers.ModelSerializer):
    priority = serializers.CharField()
    assignee_id = serializers.PrimaryKeyRelatedField(
        source="assignee", allow_null=True, queryset=User.objects.all(), required=False, write_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source="reviewer", queryset=User.objects.all(), required=False, allow_null=True, write_only=True)
    due_date = serializers.DateField(required=True)
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj) -> int:
        comments = obj.comments.count()
        return comments

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status',
                  'priority', 'reviewer_id', 'assignee_id', 'assignee', 'reviewer', 'due_date', 'comments_count']
        read_only_fields = ['id']

    def validate_assignee_id(self, value):
        return validate_board_member(self, value)

    def validate_reviewer_id(self, value):
        return validate_board_member(self, value)

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                "The due date hase to be in the future")
        return value

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.assignee:
            rep['assignee'] = MemberSerializer(instance.assignee).data
        else:
            rep['assignee'] = None
        if instance.reviewer:
            rep['reviewer'] = MemberSerializer(instance.reviewer).data
        else:
            rep['reviewer'] = None
        return rep


class BoardSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=50)
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False, write_only=True
    )
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.ReadOnlyField(source='owner.id')

    def get_member_count(self, obj) -> int:
        return obj.members.count()

    def get_ticket_count(self, obj) -> int:
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj) -> int:
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj) -> int:
        return obj.tasks.filter(priority='high').count()

    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count',
                  'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id', 'members']


class BoardDetailSerializer(BoardSerializer):
    class Meta(BoardSerializer.Meta):
        fields = ['id', 'title',
                  'owner_id', 'members']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        if request.method == 'PATCH':
            rep.pop('owner_id')
            rep['owner_data'] = MemberSerializer(instance.owner).data
            rep['members_data'] = MemberSerializer(
                instance.members.all(), many=True).data
        else:
            rep['members'] = MemberSerializer(
                instance.members.all(), many=True).data
            rep['tasks'] = TaskReadCreateSerializer(
                instance.tasks.all(), many=True).data
        return rep


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['id', 'created_at']

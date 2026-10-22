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
    """
    Serializer for representing basic user data (id, username, email)
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id', 'username', 'email']


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for handling Task data (id, board, title, description, status, priority, assignee, reviewer, due_date, comments_count')
    """
    assignee = serializers.PrimaryKeyRelatedField(
        allow_null=True, queryset=User.objects.all(), required=False, write_only=True)
    reviewer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True, write_only=True)
    due_date = serializers.DateField(required=True)
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj) -> int:
        """
        Counts the comments on the task.
        """
        count = obj.comments.count()
        return count

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority',
                  'assignee', 'reviewer', 'due_date', 'comments_count']

        read_only_fields = ['id']

    def validate_assignee(self, value):
        """
        Validate whether the chosen assignee is a member of the board.
        """
        return validate_board_member(self, value)

    def validate_reviewer(self, value):
        """
        Validate whether reviewer is a member of the board.
        """
        return validate_board_member(self, value)

    def validate_due_date(self, value):
        """
        Validate whether the provided due date is in the future.
        """
        if value <= date.today():
            raise serializers.ValidationError(
                "The due date hase to be in the future")
        return value

    def to_representation(self, instance):
        """
        Represents the assignee and reviewer using the MemberSerializer if they are set,otherwise None. 
        """
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

class TaskUpdateDeleteSerializer(TaskSerializer):
    """
    Serializer that inherits from TaskSerializer, excluding the board field
    to prevent moving the task to another board.
    """
    class Meta(TaskSerializer.Meta):
        fields = [field for field in TaskSerializer.Meta.fields if field != 'board']


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer for handling Board data (id, title, member_count, ticket_count,
                  tasks_to_do_count, tasks_high_prio_count, owner_id, members)
    """
    title = serializers.CharField(max_length=50)
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False, write_only=True
    )
    members_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.ReadOnlyField(source='owner.id')

    def get_members_count(self, obj) -> int:
        """
        Counts the members on the board.
        """
        return obj.members.count()

    def get_ticket_count(self, obj) -> int:
        """
        Counts the tasks on the board.
        """
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj) -> int:
        """
        Counts the tasks on status 'to-do' on the board.
        """
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj) -> int:
        """
        Counts the high priority task on the board.
        """
        return obj.tasks.filter(priority='high').count()

    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count',
                  'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id', 'members']


class BoardDetailSerializer(BoardSerializer):
    """
    Serializer that inherits from BoardSerializer , including only with id, title, owner_id and members fields 
    """
    class Meta(BoardSerializer.Meta):
        fields = ['id', 'title',
                  'owner_id', 'members']

    def to_representation(self, instance):
        """
        Display the Members using the MemberSerializer and the tasks using the TaskUpdateDeleteSerializer.
        If the request method is PATCH, it removes the owner_id from the response and provides full owner and member data
        """
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
            rep['tasks'] = TaskUpdateDeleteSerializer(
                instance.tasks.all(), many=True).data
        return rep


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for handling Comment data (id, created_at, content, author)
    """
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['id', 'created_at']

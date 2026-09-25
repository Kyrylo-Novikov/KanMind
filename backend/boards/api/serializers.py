from rest_framework import serializers
from django.contrib.auth.models import User
from boards.models import Board, Task


class AssignedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_login',
                  'date_joined', 'user_permissions']


class BoardSerializer(serializers.ModelSerializer):

    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return 0

    def get_tasks_to_do_count(self, obj):
        return 0

    def get_tasks_high_prio_count(self, obj):
        return 0

    class Meta:
        model = Board
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['members'] = AssignedUserSerializer(
            instance.members.all(), many=True).data
        return ret


class TaskCreatUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'


class TaskReadSerializer(serializers.ModelSerializer):
    assignee = AssignedUserSerializer(many=True, read_only=True)
    reviewer = AssignedUserSerializer(read_only=True)
    board = BoardSerializer

    class Meta:
        model = Task
        fields = '__all__'

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from board_app.models import Board, Task, Comment
from .serializers import BoardSerializer, MemberSerializer, TaskUpdateDeleteSerializer, TaskUpdateDeleteSerializer, TaskSerializer, CommentSerializer, BoardDetailSerializer
from .permissions import IsOwner, IsMember, IsAuthor, IsMemberOrOwnerOfTheBoard


class BoardListView(generics.ListCreateAPIView):
    """
    API view for listing all Boards of a user and creating new board.
    """
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieves all boards where the user is owner or member.
        """
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def perform_create(self, serializer):
        """
        Saves a new board instance and automatically assigns the requesting user as the owner.
        """
        board = serializer.save(owner=self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific board.
    """
    serializer_class = BoardDetailSerializer
    queryset = Board.objects.all()

    def get_permissions(self):
        """
        Assigns permissions based on the request method.
        Requires board ownership for DELETE requests. For other methods, member or owner permission is sufficient.
        """
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated(), (IsMember | IsOwner)()]


class EmailCheckView(APIView):
    """
    Takes the email query parameter to check if a user with this email already exists.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves email from the query params to search in db for the user
        """
        email = request.query_params.get('email')

        if not email:
            return Response(
                {'detail': 'Email query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email__iexact=email)
        serializer = MemberSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(board__members=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TaskReadCreateSerializer
        return TaskUpdateDeleteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TaskUpdateView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Task.objects.filter(board__members=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TaskReadCreateSerializer
        return TaskUpdateDeleteSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated(), (IsAuthor | IsOwner)()]
        return [IsAuthenticated(), IsMember()]


class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsMember]

    def get_task(self):
        """
        Retrieves the task from the URL and verifies that the current user is a member of the board.
        """
        task_id = self.kwargs.get('pk')
        return get_object_or_404(Task, id=task_id, board__members=self.request.user)

    def get_queryset(self):
        task = self.get_task()
        return Comment.objects.filter(task=task)

    def perform_create(self, serializer):
        task = self.get_task()
        serializer.save(author=self.request.user, task=task)


class CommentDetailView(generics.DestroyAPIView):
    permission_classes = [IsAuthor]
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_pk'

    def get_queryset(self):
        return Comment.objects.filter(task__board__members=self.request.user)


class AssignedToMeView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskReadCreateSerializer

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)


class ReviewingView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskReadCreateSerializer

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)

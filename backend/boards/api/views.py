from rest_framework import generics, status
from .serializers import BoardSerializer, AssignedUserSerializer, TaskCreatUpdateSerializer, TaskReadSerializer
from user_auth.models import UserProfile
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from boards.models import Board, Task
from rest_framework.views import APIView


class BoardListView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class EmailCheckView(APIView):

    def get(self, request):
        email = request.query_params.get('email')

        if not email:
            return Response(
                {'detail': 'E-Mail-Parameter fehlt.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            serializer = AssignedUserSerializer(user)
        except User.DoesNotExist:
            return Response({
                "detail": "Nutzer nicht gefunden"
            }, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskCreateView(generics.CreateAPIView):
    queryset = Task
    serializer_class = TaskCreatUpdateSerializer

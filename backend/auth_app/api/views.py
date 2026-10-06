from rest_framework import generics, status, views
from .serializers import RegistrationSerializer
from auth_app.models import UserProfile
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]


class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):

        data = request.data.copy()
        email = data.get('email')
        if email and not data.get('username'):
            try:
                user_obj = User.objects.get(email=email)
                data['username'] = user_obj.username
            except User.DoesNotExist:
                pass

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            print(type(Token), Token.__module__)
            user = serializer.validated_data['user']
            token, create_bool = Token.objects.get_or_create(user=user)
            data = {'token': token.key,
                    'fullname': user.username,
                    'email': user.email
                    }
            print(type(Token), Token.__module__)
            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Erfogreich ausgeloggt"}, status=status.HTTP_200_OK)

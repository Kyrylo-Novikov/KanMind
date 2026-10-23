from django.contrib.auth.models import User
from rest_framework import generics, status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import RegistrationSerializer


class RegistrationView(generics.CreateAPIView):
    """
    API view for The registration
    """
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]


class LoginView(ObtainAuthToken):
    """
    Validates email and resolves user objects for Token authentication
    """
    permission_classes = [AllowAny]

    def get_user_from_email(self, data):
        """
        Validates email and resolves user object.
        Args:
            data (dict): The request payload containing user credentials.
        Returns:
            tuple: (data, None) on success or (None, Response) on error.
        """
        data = data.copy()
        if not (email := data.get('email')):
            return None, Response({'email': ['The field is required']}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data['username'] = User.objects.get(email__iexact=email).username
            return data, None
        except User.DoesNotExist:
            return None, Response({'non_field_errors': [
                'Unable to log in with provided credentials.']},
                status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        Creates a token for the logged in user.
        Args:
            request(Request) : The HTTP request containing email and password values.
        Returns:
            Response: AJSON object with the user details and new token on seccess, or an error response if the email is missing/invalid or credentials are wrong
        """
        data, error_respons = self.get_user_from_email(request.data)
        if error_respons:
            return (error_respons)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, create_bool = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'fullname': user.username,
                             'email': user.email, 'user_id': user.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    """
    API view for The logout
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Deletes the authentication token of the logged in user to log out.

        Args:
            request (Request): The HTTP request.
        Returns:
            Response: JSON object confirming the successful logout.
        """
        request.user.auth_token.delete()
        return Response({"detail": "Erfogreich ausgeloggt"}, status=status.HTTP_200_OK)

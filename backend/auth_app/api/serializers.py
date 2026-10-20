from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    fullname = serializers.CharField(min_length=3, required=True,
                                     source='username', validators=[UniqueValidator(queryset=User.objects.all(), message="User with this name already exists.")])
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, min_length=8, required=True)
    repeated_password = serializers.CharField(
        write_only=True, min_length=8, required=True)
    token = serializers.CharField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='id', read_only=True)

    class Meta:
        model = User
        fields = ['token', 'fullname', 'email', 'password',
                  'repeated_password', 'user_id'
                  ]

    def validate_fullname(self, value):
        """
        Validates the number of words in the fullname.

        Args:
            value (str): The provided fullname string.
        Raises:
            serializers.ValidationError: If the name consists of less than 2 words.
        Returns:
            str: The stripped fullname.
        """
        stripped_name = value.strip()
        words = stripped_name.split()
        if len(words) >= 2:
            return stripped_name
        raise serializers.ValidationError(
            'The name have to consist at least 2 words')

    def validate_email(self, value):
        """
        Validates that the provided email address is not already registered.

        Args:
            value (str): The provided email address.
        Raises:
            serializers.ValidationError: If the email address is already registered.
        Returns:
            str: The validated email address.
        """
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Email already registered')
        return value

    def validate(self, values):
        """
        Validates whether both password inputs match

        Args:
            values (dict): The provided password and repeated password.
        Raises:
            serializers.ValidationError: If the passwords dont match
        Returns:
            dict: The validated values dictionary.
        """
        pw = values.get('password')
        repeated_pw = values.get('repeated_password')
        if pw != repeated_pw:
            raise serializers.ValidationError(
                {'error': ['passwords dont match']})
        return values

    def create(self, validated_data):
        """
        Creates a user, a user profile and an authentication token.

        Args:
            validated_data (dict): The validated input data containing credentials.
        Returns:
            User: The newly created user
        """
        validated_data.pop('repeated_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'])
        UserProfile.objects.create(user=user)
        token = Token.objects.create(user=user)
        user.token = token.key
        return user

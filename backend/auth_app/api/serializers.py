from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from auth_app.models import UserProfile
from rest_framework.authtoken.models import Token


class RegistrationSerializer(serializers.ModelSerializer):
    # Expose username as fullname for the frontend
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

    #   Validate the number of words in the fullname
    #   It has to consist of at least 2 words.
    def validate_fullname(self, value):
        striped_name = value.strip()
        words = striped_name.split()
        if len(words) >= 2:
            return striped_name
        else:
            raise serializers.ValidationError(
                'The name have to consist at least 2 words')

    #   Validate the given email address.
    #   It have to be a unregistered email address
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Email already registered')
        return value

    # Validate the matching of the both password inputs
    def validate(self, values):
        pw = values.get('password')
        repeated_pw = values.get('repeated_password')
        if pw != repeated_pw:
            raise serializers.ValidationError(
                {'error': ['passwords dont match']})
        return values

    # Pop repeated_password out of the validated_data and then create the User object with token
    def create(self, validated_data):
        validated_data.pop('repeated_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'])
        UserProfile.objects.create(user=user)
        token = Token.objects.create(user=user)
        user.token = token.key
        return user

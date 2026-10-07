from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from auth_app.models import UserProfile
from rest_framework.authtoken.models import Token


class RegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(min_length=3,
                                     source='username', validators=[UniqueValidator(queryset=User.objects.all(), message="User with this name already exists.")])
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)
    repeated_password = serializers.CharField(write_only=True, min_length=8)
    token = serializers.CharField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='id', read_only=True)

    class Meta:
        model = User
        fields = ['token', 'fullname', 'email', 'password',
                  'repeated_password', 'user_id'
                  ]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Email already registrated')
        return value

    def validate(self, values):
        pw = values.get('password')
        repeated_pw = values.get('repeated_password')
        if pw != repeated_pw:
            raise serializers.ValidationError(
                {'error': ' passwords dont match'})
        return values

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

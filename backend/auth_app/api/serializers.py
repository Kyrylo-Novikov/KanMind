from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from auth_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(min_length=3,
                                     source='username', validators=[UniqueValidator(queryset=User.objects.all(), message="User with this name already exists.")])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(
        queryset=User.objects.all(), message="User with this email already exists.")])
    password = serializers.CharField(write_only=True, min_length=8)
    repeated_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password',
                  'repeated_password',
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
            **validated_data)
        UserProfile.objects.create(
            user=user,
        )

        return user

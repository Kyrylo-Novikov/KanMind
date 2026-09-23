from rest_framework import serializers
from django.contrib.auth.models import User
from user_auth.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='username')
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password',
                  'repeated_password',
                  ]
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'required': True}}

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

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .validators import UsersValidatorsForCreate, UsersValidatorsForUpdate


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'password', 'password2', 'agree_to_terms'
        ]

    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    agree_to_terms = serializers.BooleanField(write_only=True, required=True)

    def validate(self, attrs):
        super_validate = super().validate(attrs)

        if self.instance:
            UsersValidatorsForUpdate(data=attrs,
                                     ErrorClass=serializers.ValidationError)
        else:
            UsersValidatorsForCreate(data=attrs,
                                     ErrorClass=serializers.ValidationError)
        return super_validate

    def create(self, validated_data):
        UserModel = get_user_model()
        user = UserModel(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

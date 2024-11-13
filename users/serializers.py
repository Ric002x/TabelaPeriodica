from django.contrib.auth import get_user_model
from rest_framework import serializers

from .validators import (ResetPasswordValidator, UsersValidatorsForCreate,
                         UsersValidatorsForUpdate)


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


class UsersChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'old_password', 'new_password', 'repeat_password'
        ]

    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    repeat_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        super_validate = super().validate(attrs)

        # Validação para old password
        User = get_user_model()
        user = User.objects.get(id=self.context['request'].user.id)

        if "old_password" in attrs:
            if not user.check_password(attrs['old_password']):
                raise serializers.ValidationError(
                    {"old_password": "A senha antiga está incorreta."}
                )
        else:
            raise serializers.ValidationError(
                {"old_password": "Campo obrigatório."}, code="blank"
            )

        # Validação para nova senha:
        ResetPasswordValidator(data=attrs,
                               ErrorClass=serializers.ValidationError)
        return super_validate

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

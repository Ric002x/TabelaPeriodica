from rest_framework import serializers

from .models import Activity
from .validators import ActivityValidator


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            'id', 'title', 'activity_slug', 'description', 'activity_link',
            'content', 'subject', 'level', 'user', 'file',
            'thumbnail'
        ]

    activity_link = serializers.HyperlinkedIdentityField(
        view_name='learn_lab:activity-api-detail',
        lookup_field='slug'
    )
    activity_slug = serializers.StringRelatedField(
        source='slug',
        read_only=True
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['subject'] = {
            "id": instance.subject.id,
            "name": instance.subject.name
        }
        representation['level'] = {
            "id": instance.level.id,
            "name": instance.level.name
        }
        representation['user'] = {
            "id": instance.user.id,
            "username": instance.user.username
        }
        return representation

    def validate(self, attrs):
        super_validade = super().validate(attrs)
        ActivityValidator(data=attrs, ErrorClass=serializers.ValidationError)
        return super_validade

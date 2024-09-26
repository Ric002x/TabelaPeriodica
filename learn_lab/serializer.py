from rest_framework import serializers

from .models import Activity
from .validators import ActivityValidator


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            'id', 'title', 'activity_slug', 'description', 'activity_link',
            'subject', 'subject_name', 'content', 'level',
            'level_name', 'user', 'user_name', 'file'
        ]

    activity_link = serializers.HyperlinkedIdentityField(
        view_name='learn_lab:activity-api-v2-detail',
        lookup_field='slug'
    )
    subject_name = serializers.StringRelatedField(
        source='subject',
        read_only=True
    )
    level_name = serializers.StringRelatedField(
        source='level',
        read_only=True
    )
    user_name = serializers.StringRelatedField(
        source='user',
        read_only=True
    )
    activity_slug = serializers.StringRelatedField(
        source='slug',
        read_only=True
    )

    def validate(self, attrs):
        super_validade = super().validate(attrs)
        ActivityValidator(data=attrs, ErrorClass=serializers.ValidationError)
        return super_validade

from rest_framework import serializers

from .models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'bio', 'local_avatar_url', 'remote_avatar_url','avatar']

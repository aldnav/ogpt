from rest_framework import serializers

from .models import GovernmentProject


class GovernmentProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentProject
        fields = ("id", "title", "project", "description")

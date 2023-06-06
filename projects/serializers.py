from rest_framework import serializers
from accounts import serializers as account_serializers
from projects import models as project_models


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = project_models.Project
        fields = ('id', 'title', 'description', 'creator', 'assignees')
        extra_kwargs = {'assignees': {'required': False}}
        read_only_fields = ('creator',)
            
    def create(self, validated_data):
        return super().create({**validated_data, 'creator': self.context['request'].user})


class ProjectGetSerializer(serializers.ModelSerializer):
    assignees = account_serializers.UserSerializer(many=True)
    creator = account_serializers.UserSerializer(many=False)
    
    class Meta:
        model = project_models.Project
        fields = ('id', 'creator', 'title', 'description', 'assignees', 'created_at', 'updated_at')

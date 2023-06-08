from projects import serializers as project_serializers


class BaseSerializerProvider:
    @classmethod
    def get_serializer_class(cls, action: str):
        raise NotImplementedError()


class ProjectSerializerProvider(BaseSerializerProvider):
    @classmethod
    def get_serializer_class(cls, action: str):
        if action in ('list', 'retrieve'):
            return project_serializers.ProjectListRetrieveSerializer
        else:  # create, update
            return project_serializers.ProjectCreateUpdateSerializer


class TaskSerializerProvider(BaseSerializerProvider):
    @classmethod
    def get_serializer_class(cls, action: str):
        if action in ('list', 'retrieve'):
            return project_serializers.TaskListRetrieveSerializer
        elif action in ('update', 'partial_update'):
            return project_serializers.TaskUpdateSerializer
        else:  # create
            return project_serializers.TaskCreateSerializer

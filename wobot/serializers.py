from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Task


class TaskSerializer(ModelSerializer):

    username = SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'createdOn',
            'deadline',
            'username',
            'complete'
        )
    
    def get_username(self, obj: Task):
        return obj.user.username
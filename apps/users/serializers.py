from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.users.models import Department

User = get_user_model()


class DepartmentSerializer(serializers.ModelSerializer):
    simple_title = serializers.CharField(required=False)

    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ('id',)

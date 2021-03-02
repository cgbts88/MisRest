from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.users.models import Department

User = get_user_model()


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ('id',)


class DepartmentForSelectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['id', 'simple_title']

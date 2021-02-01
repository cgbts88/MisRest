from rest_framework import serializers
from .models import WorkOrder, WorkOrderLog


class WorkOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    num = serializers.CharField(read_only=True, max_length=32, unique=True)
    content = serializers.CharField(max_length=512, verbose_name='内容')
    state = serializers.CharField(max_length=16, blank=True, choices=STATUS, default='wait', verbose_name='状态')
    type = serializers.CharField(max_length=16, choices=TYPES, default='normal', verbose_name='类型')
    proposer = serializers.ForeignKey(User, on_delete=models.CASCADE, verbose_name='发起人')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

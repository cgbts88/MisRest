from rest_framework import serializers
from .models import WorkOrder, WorkOrderLog


class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'
        read_only_fields = ('id', 'proposer')


class WorkOrderLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderLog
        fields = '__all__'
        read_only_fields = ('id', 'record_obj', 'recorder', 'record_time')

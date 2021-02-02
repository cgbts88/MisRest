from rest_framework import serializers
from .models import WorkOrder, WorkOrderLog


class WorkOrderSerializer(serializers.ModelSerializer):
    proposer = serializers.ReadOnlyField(source='proposer.__str__')
    state = serializers.ReadOnlyField(source='get_state_display')
    cn_type = serializers.ReadOnlyField(source='get_type_display')

    class Meta:
        model = WorkOrder
        fields = '__all__'
        read_only_fields = ('id', 'num', 'proposer')
        validators = serializers.UniqueTogetherValidator(
            queryset=WorkOrder.objects.all(),
            fields=['num']
        )

    """
    def create(self, validated_data):
        pass
    
    def update(self, instance, validated_data):
        pass
    """

    def validate_content(self, value):
        if value is None:
            raise serializers.ValidationError("Content is None")
        return value

    def validate(self, data):
        if data['content'] is None:
            raise serializers.ValidationError("Content is None")
        return data


class WorkOrderLogSerializer(serializers.ModelSerializer):
    record_obj = WorkOrderSerializer(read_only=True)
    # record_obj = serializers.ReadOnlyField(source='record_obj.num')
    recorder = serializers.ReadOnlyField(source='recorder.__str__')
    full_record_type = serializers.ReadOnlyField(source='get_record_type_display')
    # cn_record_type = serializers.SerializerMethodField()    # 用于显示模型中不存在的字段，不可反序列化

    class Meta:
        model = WorkOrderLog
        fields = '__all__'
        read_only_fields = ('id', 'record_obj', 'recorder', 'record_time')
        # depth = 1    # 设置关联模型的深度，会展示所有字段

    """
    def get_cn_record_type(self, obj):
        for item in WorkOrderLog.TYPES:
            if obj.record_type == item[0]:
                return item[1]
    """
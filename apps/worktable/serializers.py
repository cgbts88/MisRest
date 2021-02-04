from rest_framework import serializers
from .models import WorkOrder, WorkOrderLog


class WorkOrderLogSerializer(serializers.ModelSerializer):
    # record_obj = WorkOrderSerializer(read_only=True)
    record_obj = serializers.ReadOnlyField(source='record_obj.num')
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


class WorkOrderSerializer(serializers.ModelSerializer):
    created_log = serializers.SerializerMethodField('get_created_log')
    process_log = serializers.SerializerMethodField('get_process_log')
    proposer = serializers.ReadOnlyField(source='proposer.__str__')
    len_content = serializers.SerializerMethodField('get_len_content')
    state = serializers.ReadOnlyField(source='get_state_display')
    type = serializers.ReadOnlyField(source='get_type_display')
    # workorderlog_set = WorkOrderLogSerializer(many=True)

    class Meta:
        model = WorkOrder
        fields = '__all__'
        read_only_fields = ('id', 'num', 'proposer')
        validators = serializers.UniqueTogetherValidator(
            queryset=WorkOrder.objects.all(),
            fields=['num']
        )

    def get_len_content(self, obj):
        content = obj.content
        if len(str(content)) > 16:
            return '{}...'.format(str(content)[0:16])
        else:
            return str(content)

    def get_created_log(self, obj):
        try:
            log = WorkOrderLog.objects.get(record_obj=obj, record_type='create')
            serializer = WorkOrderLogSerializer(log)
            return serializer.data
        except Exception as e:
            return None

    def get_process_log(self, obj):
        try:
            log = WorkOrderLog.objects.get(record_obj=obj, record_type='process')
            serializer = WorkOrderLogSerializer(log)
            return serializer.data
        except Exception as e:
            return None

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

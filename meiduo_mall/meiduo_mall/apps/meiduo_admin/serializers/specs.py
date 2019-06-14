from rest_framework import serializers
from goods.models import SPUSpecification

class SpecsSerializer(serializers.ModelSerializer):
    # 关键属性默认输出主键，明确指定为字符串
    spu = serializers.StringRelatedField(read_only=True)
    # 隐藏属性，需要明确指定
    spu_id = serializers.IntegerField()

    class Meta:
        model = SPUSpecification
        fields = '__all__'

class SpecOptionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    value = serializers.CharField()


class SpecBySPUSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    spu = serializers.StringRelatedField(read_only=True)
    spu_id = serializers.IntegerField()
    options = SpecOptionSerializer(many=True, read_only=True)
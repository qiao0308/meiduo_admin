from rest_framework import serializers
from goods.models import SKU,SKUSpecification
from django.db import transaction
from celery_tasks.detail.tasks import generate_detail_html

class SkuSpecSerializer(serializers.Serializer):
    spec_id=serializers.IntegerField()
    option_id=serializers.IntegerField()
class SkuModelSerializer(serializers.ModelSerializer):
    spu_id=serializers.IntegerField()
    category_id=serializers.IntegerField()
    spu = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    specs=SkuSpecSerializer(many=True)
    class Meta:
        model=SKU
        fields='__all__'

    def create(self, validated_data):
        # validated_data===>接收数据后进行验证，验证后的数据存在于此字典中
        specs = validated_data.pop('specs')
        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                # 1.保存库存商品对象
                sku = super().create(validated_data)
                # 2.遍历，保存规格选项对象
                for item in specs:
                    # item===>{spec_id:***,option_id:***}
                    item['sku_id'] = sku.id
                    SKUSpecification.objects.create(**item)
            except:
                transaction.savepoint_rollback(sid)
                raise serializers.ValidationError('创建库存商品对象失败')
            else:
                transaction.savepoint_commit(sid)
                generate_detail_html.delay(sku.id)
                return sku

    def update(self, instance, validated_data):
        # instance===>需要被修改的sku对象
        # validated_data===>验证后的数据

        # 从字典中删除规格选项数据，因为模型类对应的表中没有这个字段
        specs = validated_data.pop('specs')

        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                # 1.修改sku对象
                instance = super().update(instance, validated_data)

                # 2.修改规格选项数据
                # 2.1删除sku的所有规格选项
                SKUSpecification.objects.filter(sku_id=instance.id).delete()
                # 2.2遍历
                for item in specs:
                    # 2.3创建规格选项对象
                    item['sku_id'] = instance.id
                    SKUSpecification.objects.create(**item)
            except:
                transaction.savepoint_rollback(sid)
                raise serializers.ValidationError('修改sku失败')
            else:
                transaction.savepoint_commit(sid)
                generate_detail_html.delay(instance.id)
                return instance
class SkuSimpleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()














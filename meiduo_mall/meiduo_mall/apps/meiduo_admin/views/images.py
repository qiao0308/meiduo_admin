from rest_framework.viewsets import ModelViewSet
from goods.models import SKUImage
from meiduo_admin.serializers.images import ImageModelSerializer
from meiduo_admin.utils.pagination import MeiduoPagination
from rest_framework import serializers
from fdfs_client.client import Fdfs_client
from django.conf import settings
# from meiduo_mall.settings import dev
from rest_framework.response import Response
from celery_tasks.detail.tasks import generate_detail_html

class ImageModelViewSet(ModelViewSet):
    queryset = SKUImage.objects.all().order_by('-id')
    serializer_class = ImageModelSerializer
    pagination_class = MeiduoPagination

    def create(self, request, *args, **kwargs):
        # 1.接收
        sku_id = request.data.get('sku')
        image_file = request.data.get('image')

        # 2.验证
        if not all([sku_id, image_file]):
            serializers.ValidationError('数据不完整')

        # 3.处理1：上传图片
        client = Fdfs_client(settings.FDFS_CLIENT_PATH)
        ret = client.upload_by_buffer(image_file.read())
        if ret['Status'] != 'Upload successed.':
            raise serializers.ValidationError('上传失败')
        # 3....获取文件名
        image_name = ret['Remote file_id']

        # 4.处理2：创建对象
        image = SKUImage.objects.create(sku_id=sku_id, image=image_name)
        sku = image.sku
        if not sku.default_image:
            sku.default_image = image.image
            sku.save()

            generate_detail_html.delay(sku.id)
        # 5.响应
        serializer = self.get_serializer(image)
        return Response(serializer.data, status=201)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 1.删数据
        instance.delete()
        # 2.删图片
        client = Fdfs_client(settings.FDFS_CLIENT_PATH)
        client.delete_file(instance.image.name)

        return Response(status=204)

    def update(self, request, *args, **kwargs):
        # 1.接收
        sku_id = request.data.get('sku')
        image_file = request.data.get('image')

        # 2.验证
        if not all([sku_id, image_file]):
            raise serializers.ValidationError('参数不全')

        # 3.1处理：查询对象
        instance = self.get_object()

        # 3.2处理：图片（删，传）
        client = Fdfs_client(settings.FDFS_CLIENT_PATH)
        client.delete_file(instance.image.name)
        ret = client.upload_by_buffer(image_file.read())
        if ret['Status'] != 'Upload successed.':
            raise serializers.ValidationError('上传失败')
        image_name = ret['Remote file_id']

        # 3.3处理：修改
        instance.sku_id = sku_id
        instance.image = image_name
        instance.save()

        # 4.响应
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=201)





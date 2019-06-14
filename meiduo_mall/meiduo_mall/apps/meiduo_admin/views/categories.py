from rest_framework import generics
from goods.models import GoodsCategory
from meiduo_admin.serializers.categories import Category3Serializer


class Category3View(generics.ListAPIView):
    queryset = GoodsCategory.objects.filter(subs__isnull=True)

    serializer_class = Category3Serializer
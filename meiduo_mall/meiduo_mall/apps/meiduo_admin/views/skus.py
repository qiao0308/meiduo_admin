from rest_framework.viewsets import ModelViewSet
from goods.models import SKU
from meiduo_admin.serializers.skus import SkuModelSerializer,SkuSimpleSerializer
from meiduo_admin.utils.pagination import MeiduoPagination
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response


class SkuModelViewSet(ModelViewSet):
    # queryset =
    def get_queryset(self):
        # return SKU.objects.all().order_by('-id')
        queryset = SKU.objects
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(Q(name__contains=keyword) | Q(caption__contains=keyword))
        queryset = queryset.order_by('-id')
        return queryset
    serializer_class = SkuModelSerializer
    pagination_class = MeiduoPagination
    @action(methods=['get'], detail=False)
    def simple(self, request):
        queryset = self.get_queryset()
        serializer = SkuSimpleSerializer(queryset, many=True)
        return Response(serializer.data)








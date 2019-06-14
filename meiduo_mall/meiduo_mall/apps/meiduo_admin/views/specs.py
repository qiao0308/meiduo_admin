from rest_framework import generics
from goods.models import SPUSpecification
from meiduo_admin.serializers.specs import SpecsSerializer, SpecBySPUSerializer
from meiduo_admin.utils.pagination import MeiduoPagination
from rest_framework.viewsets import ModelViewSet

class SpecsView(generics.ListCreateAPIView):
    queryset=SPUSpecification.objects.all()
    serializer_class = SpecsSerializer
    pagination_class = MeiduoPagination
class SpecView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SPUSpecification.objects.all()
    serializer_class = SpecsSerializer
class SpecsModelViewSet(ModelViewSet):
    queryset = SPUSpecification.objects.all()
    serializer_class = SpecsSerializer
    pagination_class = MeiduoPagination


class SpecBySPUView(generics.ListAPIView):
    def get_queryset(self):
        # 从请求路径中获取spu的id
        spu_id = self.kwargs.get('pk')
        # 查询指定spu_id的规格
        queryset = SPUSpecification.objects.filter(spu_id=spu_id)
        return queryset

    serializer_class = SpecBySPUSerializer
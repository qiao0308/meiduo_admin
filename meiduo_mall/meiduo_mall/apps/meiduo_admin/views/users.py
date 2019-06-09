from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from users.models import User
from meiduo_admin.serializers.users import UserSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from meiduo_admin.utils.pagination import MeiduoPagination


# class UsersView(APIView):
#     # permission_classes = [IsAdminUser]
#
#     def get(self, request):
#         request.query_params.get()
#         queryset = User.objects.filter(is_staff=False).order_by('-id')
#
#         serializer = UserSerializer(queryset, many=True)
#
#         return Response(serializer.data)

class UsersView(generics.ListAPIView):
    # 说明：需要通过视图对象获得请求对象，再获取参数
    # 使用queryset属性时，这是个类属性，无法访问实例属性
    # 使用get_queryset方法时，这是个实例方法，可以访问实例属性
    # queryset = User.objects.filter(is_staff=False,username__contains=).order_by('-id')
    def get_queryset(self):
        # self.request,self.args,self.kwargs
        # 普通会员
        queryset = User.objects.filter(is_staff=False)
        # 查询用户名条件
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(username__contains=keyword)
        # 排序：最新的放在最前面
        queryset = queryset.order_by('-id')
        # 返回查询集
        return queryset

    serializer_class = UserSerializer

    # 分页
    pagination_class = MeiduoPagination
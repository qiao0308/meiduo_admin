from rest_framework.views import APIView
# 返回
from rest_framework.response import Response
# 权限认证
from rest_framework.permissions import IsAuthenticated
from users.models import User
from datetime import date


class TotalView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        count=User.objects.filter(is_staff=False).count()
        today=date.today()
        return Response({
            'count':count,
            'date':today
        })

class IncrementView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        today=date.today()
        count=User.objects.filter(is_staff=False,date_joined__gte=today).count()
        return Response({
            'count': count,
            'date': today
        })


class ActiveView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        # 日活跃用户统计
        today = date.today()
        # 今天登录过的用户
        # 今天登录过的用户
        count=User.objects.filter(is_staff=False,last_login__gte=today).count()
        return Response({
            'count': count,
            'date': today
        })
class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        # 日下单用户量统计
        today = date.today()
        # 今天下单的用户数量
        count = User.objects.filter(orders__create_time__gte=today).count()
        return Response({
            'count': count,
            'date': today
        })







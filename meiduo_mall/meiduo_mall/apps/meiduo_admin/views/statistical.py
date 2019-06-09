from rest_framework.views import APIView
# 返回
from rest_framework.response import Response
# 权限认证
from rest_framework.permissions import IsAuthenticated
from users.models import User
from datetime import date, timedelta


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

class MonthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 月增用户统计：在过去的一个月，每天有多少新增用户
        today = date.today()
        # 定义列表，存在每天的人数
        month_list = []
        # 计算一个月（30天）中的第一天
        month_day1 = today - timedelta(days=29)
        # 遍历，30天
        for i in range(30):  # [0,29]
            # 某天的开始、结束
            begin_date = month_day1 + timedelta(days=i)
            end_date = month_day1 + timedelta(days=i + 1)
            # 统计某天的新增人数
            count = User.objects.filter(is_staff=False, date_joined__gte=begin_date, date_joined__lt=end_date).count()
            month_list.append({
                'count': count,
                'date': begin_date
            })

        return Response(month_list)





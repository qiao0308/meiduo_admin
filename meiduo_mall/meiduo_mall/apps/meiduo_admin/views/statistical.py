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

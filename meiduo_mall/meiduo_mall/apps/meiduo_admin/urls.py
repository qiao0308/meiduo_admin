from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from .views import users
from . import views
from .views import statistical
urlpatterns = [
    url('^authorizations/$',obtain_jwt_token),
    url('^statistical/total_count/$', statistical.TotalView.as_view()),
    url('^statistical/day_increment/$', statistical.IncrementView.as_view()),
    url('^statistical/day_active/$', statistical.ActiveView.as_view()),
    url('^statistical/day_orders/$', statistical.OrderView.as_view()),
url('^statistical/month_increment/$', statistical.MonthView.as_view()),
    url('^statistical/goods_day_views/$', statistical.GoodsView.as_view()),
    url('^users/$', users.UsersView.as_view()),
]

from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from .views import users,specs,spus,skus,categories,images
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
    # url('^goods/specs/$', specs.SpecsView.as_view()),
    url('^goods/simple/$', spus.SPUSimpleView.as_view()),
url('^skus/categories/$', categories.Category3View.as_view()),
    # url('^goods/specs/(?P<pk>\d+)/$', specs.SpecView.as_view()),
    url('^goods/(?P<pk>\d+)/specs/$', specs.SpecBySPUView.as_view()),
]
router = DefaultRouter()
router.register('goods/specs', specs.SpecsModelViewSet, base_name='specs')
router.register('skus/images', images.ImageModelViewSet, base_name='images')
router.register('skus', skus.SkuModelViewSet, base_name='skus')



urlpatterns += router.urls
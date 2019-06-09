from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import views
from .views import statistical
urlpatterns = [
    url('^authorizations/$',obtain_jwt_token),
    url('^statistical/total_count/$', statistical.TotalView.as_view()),



]

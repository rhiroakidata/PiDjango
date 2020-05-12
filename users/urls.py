from users import views
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    url(r'^api/users$', views.users_list),
    url(r'^api/users/(?P<pk>[0-9]+)$', views.users_detail),
    url('login', views.login),
]
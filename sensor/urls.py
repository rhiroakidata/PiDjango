from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url('turnOn', views.turnOn, name='turnOn'),
    url('gas_sensor', views.gasSensor, name='gasSensor'),
    url('gps_sensor', views.gpsSensor, name='gpsSensor'),
    url('dht11_sensor', views.dht11Sensor, name='dht11Sensor'),
    url('photo_sensor', views.photoSensor, name='photoSensor'),
    url('distance_sensor', views.distanceSensor, name='distanceSensor'),
    url('index', views.index, name='index'),
    url('camera', views.camera, name='camera'),
    #url(r'^take_photo/(?P<pk>[0-9]+)$', views.take_photo)
]
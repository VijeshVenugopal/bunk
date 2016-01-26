from django.conf.urls import include, url
from bunkapp import views

urlpatterns = [
    url(r'^dashboard/$',views.dashboard,name='login')
]

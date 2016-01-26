from django.conf.urls import include, url
from bunkapp.views import *

urlpatterns = [
	#url(r'/$',LandingPage.as_view(),name='landing_page'),
    url(r'^$',LandingView.as_view()),
    url(r'^dashboard/$',dashboard,name='dashboard'),
    url(r'^login/$',LoginView.as_view(),name='login'),
    #url(r'^logout/$',LogoutView.as_view(),name='logout'),
]

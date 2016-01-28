from django.conf.urls import include, url
from petroapp.views import *

urlpatterns = [
    url(r'^entries/$', EntryListView.as_view(), name="entry-list"),
    #url(r'^(?P<username>\w+)/$',UserEntryView.as_view(), name="user_entry"),
    url(r'^attendance/$', AttendanceCreateView.as_view(), name="attendance_create"),


]

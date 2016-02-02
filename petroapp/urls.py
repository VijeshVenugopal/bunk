from django.conf.urls import include, url
from petroapp.views import *

urlpatterns = [
    url(r'^entries/$', EntryListView.as_view(), name="entry-list"),
    #url(r'^(?P<username>\w+)/$',UserEntryView.as_view(), name="user_entry"),
    url(r'^attendance/$', AttendanceCreateView.as_view(), name="attendance_create"),
    url(r'attendance/(?P<pk>[0-9]+)/$', AttendenceClose.as_view(), name='attendence-close'),
    url(r'^petro-details/$', PetroAdminListView.as_view(), name="petroadmin-list"),
    url(r'^fill-petrol/$', PetroFillView.as_view(), name="petro-fill"),
    url(r'^update-petrol/(?P<pk>[0-9]+)/$', PetroUpdateView.as_view(), name="petro-update"),
]


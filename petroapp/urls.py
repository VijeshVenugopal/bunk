from django.conf.urls import include, url
from petroapp.views import *

urlpatterns = [
    url(r'^entries/$', EntryListView.as_view(), name="entry-list"),
    url(r'^attendance/$', AttendanceCreateView.as_view(), name="attendance_create"),
    url(r'attendance/(?P<pk>[0-9]+)/$', AttendenceClose.as_view(), name='attendence-close'),
    url(r'^add-details/$', EmployeeEntryView.as_view(), name="employee-entry"),
    url(r'^petro-details/$', PetroAdminListView.as_view(), name="petroadmin-list"),
    url(r'^list-red/$', PetroRedListView.as_view(), name="petrotype-red"),
    url(r'^list-green/$', PetroGreenListView.as_view(), name="petrotype-green"),
    url(r'^fill-petrol/$', PetroFillView.as_view(), name="petro-fill"),
    url(r'^update-petrol/(?P<pk>[0-9]+)/$', PetroUpdateView.as_view(), name="petro-update"),
    url(r'employees/$', EmployeesListView.as_view(), name="employee_list"),
    url(r'^registration/$', MyRegistrationView.as_view(), name="employee_registration"),
    url(r'^expenses/list$',ExpenseListView.as_view(), name="expenses_list"),
    url(r'^expenses/$',ExpenseView.as_view(), name="expenses_record"),
    url(r'^stock/$',StockView.as_view(), name="stock_balance"),
    url(r'bunk-detail/(?P<pk>[0-9]+)/$', BunkDetailView.as_view(), name='bunk-detail'),
]


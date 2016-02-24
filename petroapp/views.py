from datetime import date, datetime
from datetime import timedelta
from django.shortcuts import render
from django.views.generic import View
from django.views.generic import CreateView, ListView,UpdateView, DetailView
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.db.models import Sum
from django.contrib.auth.models import User
from django.template.context import RequestContext
from registration.backends.simple.views import RegistrationView

from petroapp.forms import *


class MyRegistrationView(RegistrationView):
    def get_success_url(self, request):
        return "/employees"

class EntryListView(ListView):
    model = DailyInputs
    template_name = "employee/entry_list.html"

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
        try:
            context['emp_status'] = AttendanceRecord.objects.get(date=date.today(),user=self.request.user)
            emp_status = AttendanceRecord.objects.get(date=date.today(),user=self.request.user)
            if emp_status.status == True:
                context['status'] = 'in'
            else:
                context['status'] = 'out'
            if emp_status.checkin_time:
                if emp_status.checkout_time:
                    if emp_status.date == date.today():
                        context['getout'] = 'True'
        except:
            context['status'] = 'out'
        context['entries'] = AttendanceRecord.objects.filter(user=self.request.user)
        return context


"""
class UserEntryView(View):
    template_name = "employee/employee_entry.html"   

    def get(self, request, *args, **kwargs):
        form = EmployeeEntryForm()
	context = {}
	context['form'] = form
	return render(self.request,self.template_name, context)

    def post(self, request, *args, **kwargs):
	form = EmployeeEntryForm(request.POST)
	if form.is_valid():
	    entry = form.save(commit=False)
	    entry.user = self.request.user
            entry.save()
	    messages.success(self.request, "entry added successfully")
	    return HttpResponseRedirect(reverse('entry-list'))

    def get_context_data(self, **kwargs):
        context = super(UserEntryView, self).get_context_data(**kwargs)
        return context
"""

class AttendanceCreateView(CreateView):
    model = AttendanceRecord
    form_class = AttendanceRecordForm
    template_name = "employee/employee_attendance.html"

    def form_valid(self,form):
        attendance = form.save(commit=False)
        attendance.user = self.request.user
        attendance.date = date.today()
        attendance.status = True
        attendance.checkin_time = timezone.now()
        attendance.save()
        return HttpResponseRedirect(reverse("entry-list"))

class EmployeeEntryView(CreateView):
    model = AttendanceRecord
    form_class = AttendanceEntryForm
    template_name = "petroadmin/employee-entry.html"

    def form_valid(self, form):
        attendance = form.save(commit=False)
        attendance.status = True
        attendance.checkin_time = timezone.now()
        attendance.checkout_time = timezone.now()
        attendance.save()
        mach = Machine.objects.get(petro_bunk=attendance.petro_bunk.id, name=attendance.machine.name)
        dif = attendance.end_reading-attendance.start_reading
        #fuel_total=FuelRecords.objects.filter(fu_type=mach.fuel).aggregate(num_litres=Sum('litre')-(attendance.end_reading-	attendance.start_reading))
        try:
            fuel_obj = FuelRecords.objects.get(fu_type=mach.fuel)
        except:
            fuel_obj = FuelRecords.objects.filter(fu_type=mach.fuel)[0]
            fuel_obj.litre -= dif
            fuel_obj.save()
        return HttpResponseRedirect(reverse('petroadmin-list'))

class AttendenceClose(UpdateView):
    model = AttendanceRecord
    form_class = AttendanceRecordCloseForm
    #success_url="/employee/entries/"
    template_name = "employee/employee_attendance.html"
    def form_valid(self,form):
        attendance = form.save(commit=False)
        attendance.checkout_time = timezone.now()
        attendance.save()
        return HttpResponseRedirect(reverse("entry-list"))

    def get_context_data(self, **kwargs):
        context = super(AttendenceClose, self).get_context_data(**kwargs)
        emp_status = AttendanceRecord.objects.get(date=date.today(),user=self.request.user)
        if emp_status.status == True:
            context['alreadyin'] = 'alreadyin'
        return context

class PetroAdminListView(TemplateView):
    template_name = "petroadmin/petro-list.html"

    def get_context_data(self, **kwargs):
        context = super(PetroAdminListView, self).get_context_data(**kwargs)
        context['objects'] = DailyInputs.objects.all()
        #context['redentries'] = FuelRecords.objects.filter(fu_type="red", added_time__lte=datetime.datetime.now()).aggregate(Sum('litre'))
        #context['greenentries'] = FuelRecords.objects.filter(fu_type="green", added_time__lte=datetime.datetime.now()).aggregate(Sum('litre'))
        #context['totalcollection'] = AttendanceRecord.objects.filter(date=date.today()).aggregate(Sum('collection'))
	context['attendance_objs'] = AttendanceRecord.objects.all()
	context['bunks'] = PetroBunk.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        bunk_id = self.request.POST['bunk']
        recs = AttendanceRecord.objects.filter(petro_bunk_id=bunk_id)
	context = {}
	context['form'] = MyBunkForm()
	if recs:
	    for r in recs:
     	        if r.machine.fuel == "red":
 		    context['red_start'] = r.start_reading
		    context['red_end'] = r.end_reading
		    context['red_total'] = r.collection
		    context['red_diff'] = r.end_reading - r.start_reading
	        if r.machine.fuel == "green":
		    context['green_start'] = r.start_reading
		    context['green_end'] = r.end_reading
		    context['green_total'] = r.collection
		    context['green_diff'] = r.end_reading - r.start_reading
		
	return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        context = super(PetroAdminListView, self).get_context_data(**kwargs)
        context['form'] = MyBunkForm()
        return self.render_to_response(context)

    

class PetroFillView(CreateView):
    model = FuelRecords
    form_class = PetroFillForm
    template_name = "petroadmin/petro-fill.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.added_time = timezone.now()
        obj.save()
        return HttpResponseRedirect(reverse('petro-fill-list'))

class PetroUpdateView(UpdateView):
    model = FuelRecords
    form_class = PetroFillForm
    template_name = "petroadmin/petro-fill.html"

    def get(self, request, *args, **kwargs):
        self.object = FuelRecords.objects.get(id=self.kwargs['pk'])
	form_class = self.get_form_class()
	form = self.get_form(form_class)
	context = self.get_context_data(object=self.object, form=form)
	return self.render_to_response(context)

    def form_valid(self, form):
        obj = form.save(commit=False)
	obj.added_time = timezone.now()
	obj.save()
	return HttpResponseRedirect(reverse('petroadmin-list'))

class EmployeesListView(ListView):
    model = User
    template_name = "admin/employees_list.html"

    def get_context_data(self, **kwargs):
        context = super(EmployeesListView, self).get_context_data(**kwargs)
        context['employees'] = User.objects.all().exclude(is_superuser=True)
        return context

class PetroRedListView(ListView):
    model = FuelRecords
    template_name = "petroadmin/petrored-list.html"

    def get_context_data(self, *args, **kwargs):
	context = super(PetroRedListView, self).get_context_data(**kwargs)
	context['redarrivals'] = FuelRecords.objects.filter(date__gte=datetime.datetime.now()-timedelta(days=7), fu_type="red")
	return context


class PetroGreenListView(ListView):
    model = FuelRecords
    template_name = "petroadmin/petrogreen-list.html"

    def get_context_data(self, *args, **kwargs):
	context = super(PetroGreenListView, self).get_context_data(**kwargs)
	context['greenarrivals'] = FuelRecords.objects.filter(date__gte=datetime.datetime.now()-timedelta(days=7), fu_type="green")
	return context

class ExpenseView(CreateView):
    model = ExpenseRecord
    form_class = ExpenseRecordForm
    template_name = "petroadmin/expense-record.html"

    def form_valid(self,form):
        expense = form.save(commit=False)
        expense.save()
        return HttpResponseRedirect(reverse("expenses_list"))

class ExpenseListView(ListView):
    model = ExpenseRecord
    template_name = "petroadmin/expense-list.html"
    def get_context_data(self, *args, **kwargs):
        context = super(ExpenseListView, self).get_context_data(**kwargs)
        context['objects_list'] = ExpenseRecord.objects.all()
        return context

class StockView(ListView):
    model = ExpenseRecord
    template_name = "petroadmin/stock-balance.html"
    def get_context_data(self, *args, **kwargs):
        context = super(StockView, self).get_context_data(**kwargs)
        context['objects_list'] = ExpenseRecord.objects.all()
        return context

class PetroFillListView(ListView):
    model = FuelRecords
    template_name = "petroadmin/fill_list.html"
    def get_context_data(self, *args, **kwargs):
        context = super(PetroFillListView, self).get_context_data(**kwargs)
        context['objects_list'] = FuelRecords.objects.all()
        return context

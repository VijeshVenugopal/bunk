from datetime import date
from django.shortcuts import render
from django.views.generic import View
from django.views.generic import CreateView, ListView,UpdateView
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.db.models import Sum

from petroapp.forms import *

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
	context['redentries'] = FuelRecords.objects.filter(fu_type="red").aggregate(Sum('litre'))
	context['greenentries'] = FuelRecords.objects.filter(fu_type="green").aggregate(Sum('litre'))
	return context

class PetroFillView(CreateView):
    model = FuelRecords
    form_class = PetroFillForm
    template_name = "petroadmin/petro-fill.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
	obj.added_time = timezone.now()
	obj.save()
        return HttpResponseRedirect(reverse('petroadmin-list'))

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

from datetime import date
from django.shortcuts import render
from django.views.generic import View
from django.views.generic import CreateView, ListView
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from petroapp.forms import *

class EntryListView(ListView):
    model = DailyInputs
    template_name = "employee/entry_list.html"

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
	context['entries'] = DailyInputs.objects.all()	
	return context


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
	    entries = DailyInputs.objects.filter(date__startswith=date.today())	
            return render(self.request,self.template_name,{'form':EmployeeEntryForm(), 'entries':entries})



from datetime import date
from django.shortcuts import render
from django.views.generic import View
from django.views.generic import CreateView, ListView
from django.http import HttpResponse
from django.contrib import messages

from petroapp.forms import *

class EntryListView(ListView):
    model = DailyInputs
    template_name = "employee/entry_list.html"

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
	context['entries'] = DailyInputs.objects.filter(date__startswith=date.today())	
	print context
	return context


class UserEntryView(CreateView):
    model = DailyInputs
    form_class = EmployeeEntryForm
    template_name = "employee/employee_entry.html"     

    def form_valid(self, form):
	entry = form.save(commit=False)
	entry.user = self.request.user
	entry.save()
	messages.success(self.request, "entry added successfully")
        return render(self.request,self.template_name,{'form':EmployeeEntryForm()})


    def get_context_data(self, **kwargs):
        context = super(UserEntryView, self).get_context_data(**kwargs)
        return context

from django import forms
from django.forms import ModelForm
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget

from petroapp.models import *

class EmployeeEntryForm(ModelForm):
    
    class Meta:
        model = DailyInputs
        exclude = ('user', 'date')



class AttendanceEntryForm(ModelForm):
	date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3)) 
	collection = forms.DecimalField(required=True)

	class Meta:
		model = AttendanceRecord
		exclude = ()
	def __init__(self, *args, **kwargs):
		super(AttendanceEntryForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
		    field.widget.attrs['class'] = 'form-control'
		#self.fields['user'].queryset = Employees.objects.exclude(is_superuser=True)
		self.fields['start_reading_red'].label = "Start Reading Red"
		self.fields['end_reading_red'].label = "End Reading Red" 
		self.fields['start_reading_green'].label = "Start Reading Green"
		self.fields['end_reading_green'].label = "End Reading Green" 
		self.fields['start_reading_diesel'].label = "Start Reading Diesel"
		self.fields['end_reading_diesel'].label = "End Reading Diesel" 

class AttendanceRecordCloseForm(ModelForm):
	class Meta:
		model = AttendanceRecord
		fields = ('end_reading_red','collection')
	def __init__(self, *args, **kwargs):
		super(AttendanceRecordCloseForm, self).__init__(*args, **kwargs)
		self.fields['end_reading'].widget.attrs.update({'class':'form-control'})
		self.fields['collection'].widget.attrs.update({'class':'form-control'})

class PetroFillForm(ModelForm):
	date = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3)) 
	class Meta:
		model = FuelRecords
		fields = ('date','bunk','fu_type', 'litre', 'description','veh_num')
	
	def __init__(self, *args, **kwargs):
		super(PetroFillForm, self).__init__(*args, **kwargs)
		self.fields['date'].widget.attrs.update({'class':'form-control'})
		self.fields['bunk'].widget.attrs.update({'class':'form-control'})
		self.fields['fu_type'].widget.attrs.update({'class':'form-control'})
		self.fields['litre'].widget.attrs.update({'class':'form-control'})
		self.fields['veh_num'].widget.attrs.update({'class':'form-control'})
		self.fields['description'].widget.attrs.update({'class':'form-control'})

class PetroFuelFillForm(ModelForm):
	date = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3)) 
	class Meta:
		model = FuelFillRecords
		exclude = ('added_time',)
	
	def __init__(self, *args, **kwargs):
		super(PetroFuelFillForm, self).__init__(*args, **kwargs)
		self.fields['date'].widget.attrs.update({'class':'form-control'})
		self.fields['bunk'].widget.attrs.update({'class':'form-control'})
		self.fields['red_litre'].widget.attrs.update({'class':'form-control'})
		self.fields['green_litre'].widget.attrs.update({'class':'form-control'})
		self.fields['diesel_litre'].widget.attrs.update({'class':'form-control'})
		self.fields['veh_num'].widget.attrs.update({'class':'form-control'})
		self.fields['description'].widget.attrs.update({'class':'form-control'})

class ExpenseRecordForm(ModelForm):
	date = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3)) 
	class Meta:
		model = ExpenseRecord
		fields = ('bunk','date','reason','amount','receiver')
	def __init__(self, *args, **kwargs):
		super(ExpenseRecordForm, self).__init__(*args, **kwargs)
		self.fields['bunk'].widget.attrs.update({'class':'form-control'})
		self.fields['reason'].widget.attrs.update({'class':'form-control'})
		self.fields['amount'].widget.attrs.update({'class':'form-control'})
		self.fields['receiver'].widget.attrs.update({'class':'form-control'})
		
class MyBunkForm(forms.Form):
	bunk = forms.ModelChoiceField(queryset=PetroBunk.objects.all())

	def __init__(self, *args, **kwargs):
		super(MyBunkForm, self).__init__(*args, **kwargs)
		self.fields['bunk'].widget.attrs.update({'class':'form-control'})
		self.fields['bunk'].label="Select Bunk"

class EmployeeCreateForm(ModelForm):
	
	class Meta:
		model = Employees
		exclude = ('added_date',)

	def __init__(self, *args, **kwargs):
		super(EmployeeCreateForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
		    field.widget.attrs['class'] = 'form-control'



from django import forms
from django.forms import ModelForm
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget

from petroapp.models import *

class EmployeeEntryForm(ModelForm):
    
    class Meta:
        model = DailyInputs
        exclude = ('user', 'date')

class AttendanceRecordForm(ModelForm):
	class Meta:
		model = AttendanceRecord
		fields = ('machine','start_reading')
	def __init__(self, *args, **kwargs):
		super(AttendanceRecordForm, self).__init__(*args, **kwargs)
		self.fields['machine'].widget.attrs.update({'class':'form-control'})
		self.fields['start_reading'].widget.attrs.update({'class':'form-control'})

class AttendanceEntryForm(ModelForm):
	collection = forms.DecimalField(required=True) 
	class Meta:
		model = AttendanceRecord
		exclude = ('status','date','checkin_time','checkout_time')
	def __init__(self, *args, **kwargs):
		super(AttendanceEntryForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
		    field.widget.attrs['class'] = 'form-control'
		self.fields['user'].queryset = User.objects.exclude(is_superuser=True)

class AttendanceRecordCloseForm(ModelForm):
	class Meta:
		model = AttendanceRecord
		fields = ('end_reading','collection')
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


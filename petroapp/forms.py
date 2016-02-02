from django import forms
from django.forms import ModelForm

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

class AttendanceRecordCloseForm(ModelForm):
	class Meta:
		model = AttendanceRecord
		fields = ('end_reading','collection')
	def __init__(self, *args, **kwargs):
		super(AttendanceRecordCloseForm, self).__init__(*args, **kwargs)
		self.fields['end_reading'].widget.attrs.update({'class':'form-control'})
		self.fields['collection'].widget.attrs.update({'class':'form-control'})

class PetroFillForm(ModelForm):
	class Meta:
		model = FuelRecords
		fields = ('fu_type', 'litre', 'description', 'veh_num')

		def __init__(self, *args, **kwargs):
			super(PetroFillForm, self).__init__(*args, **kwargs)
			self.fields['fu_type'].widget.attrs['class'] = 'form-control'
			self.fields['litre'].widget.attrs['class'] = 'form-control'
			self.fields['description'].widget.attrs['class'] = 'form-control'

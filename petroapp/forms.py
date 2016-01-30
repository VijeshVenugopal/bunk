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
		exclude = ('user','date','checkin_time','checkout_time','status')
	def __init__(self, *args, **kwargs):
		super(AttendanceRecordForm, self).__init__(*args, **kwargs)
		self.fields['machine'].widget.attrs.update({'class':'form-control'})
		self.fields['start_reading'].widget.attrs.update({'class':'form-control'})
		self.fields['end_reading'].widget.attrs.update({'class':'form-control'})
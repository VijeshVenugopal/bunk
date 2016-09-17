import datetime

from django.db import models
from django.contrib.auth.models import User

class PetroBunk(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "PetroBunk"
	verbose_name_plural = "PetroBunks"

    def __unicode__(self):
        return self.name

class Employees(models.Model):
    bunk = models.ForeignKey(PetroBunk)
    name = models.CharField(max_length=50,null=True,blank=True)
    phone_number = models.CharField(max_length=50,null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    added_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Machine(models.Model):
    """
    Model for machines.
    """
    CHOICES = (
        ('red', 'RED'),
        ('green', 'GREEN'),    
    )
    petro_bunk = models.ForeignKey(PetroBunk)
    name = models.CharField(max_length=50)
    fuel = models.CharField(max_length=5, choices=CHOICES)
    class Meta:
        verbose_name = "Machine"
        verbose_name_plural = "Machines"

    def __unicode__(self):
        return self.name

class DailyInputs(models.Model):
    """
    Models for storing daily activities of user.
    """
    CHOICES = (
        ('red', 'RED'),
        ('green', 'GREEN'),    
	)
    user = models.ForeignKey(User, related_name='user_set')
    machine = models.ForeignKey(Machine, related_name="machines")
    start_reading = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    end_reading = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    price = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=5, choices=CHOICES)

    class Meta:
        verbose_name = "Daily Detail"
        verbose_name_plural = "Daily Details"

    def __unicode__(self):
        return str(self.user)

class FuelAvailability(models.Model):
    """
    Models for storing fuel levels in each machine.
    """
    CHOICES = (
        ('red', 'RED'),
        ('green', 'GREEN'),    
	)
    petro_bunk = models.ForeignKey(PetroBunk, related_name="bunks")
    machine_fuel = models.ForeignKey(Machine, related_name="machine_fuel")
    litre = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    fu_type = models.CharField(max_length=5, choices=CHOICES)

    class Meta:
        verbose_name = "Fuel Availability"
        verbose_name_plural = "Fuel Availabilities"

    def __unicode__(self):
        return str(self.litre)

class AttendanceRecord(models.Model):
    CHOICES = (
	('s1','SHIFT1'),
	('s2','SHIFT2')
	)
    shift_type = models.CharField(max_length=10, choices=CHOICES)
    petro_bunk = models.ForeignKey(PetroBunk, related_name="petrobunks",null=True,blank=True)
    machine = models.ForeignKey(Machine, related_name="machines_input")
    status = models.BooleanField(default=False)
    date = models.DateField(null=True,blank=True,default=datetime.date.today)
    start_reading_red = models.DecimalField(max_digits=20, decimal_places=5,null=True,blank=True)
    end_reading_red = models.DecimalField(max_digits=20, decimal_places=5,null=True,blank=True)
    sales_collection_red = models.DecimalField(max_digits=20, decimal_places=5,null=True,blank=True)
    start_reading_green = models.DecimalField(max_digits=20, decimal_places=5,null=True,blank=True)
    end_reading_green = models.DecimalField(max_digits=20, decimal_places=5,null=True,blank=True)
    sales_collection_green = models.DecimalField(max_digits=20, decimal_places=5,null=True,blank=True)
    start_reading_diesel = models.DecimalField(max_digits=20, decimal_places=5,null=True,blank=True)
    end_reading_diesel = models.DecimalField(max_digits=20, decimal_places=5,null=True,blank=True)
    sales_collection_diesel = models.DecimalField(max_digits=20, decimal_places=5,null=True,blank=True)
    actual_amount = models.DecimalField(max_digits=9, decimal_places=5,null=True,blank=True)
    collection = models.DecimalField(max_digits=9, decimal_places=5,null=True,blank=True)

    def __unicode__(self):
        return str(self.date)

class FuelRecords(models.Model):
    """
       Models for storing fule records.
    """
    CHOICES = (
        ('red', 'RED'),
        ('green', 'GREEN'),    
	)
    bunk = models.ForeignKey(PetroBunk,null=True,blank=True)
    date = models.DateTimeField(null=True,blank=True)
    fu_type = models.CharField(max_length=5, choices=CHOICES)
    litre = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    veh_num = models.CharField(max_length=50, null=True, blank=True)
    added_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.date)

class FuelFillRecords(models.Model):
    """
       Models for storing fuel fill records.
    """
    bunk = models.ForeignKey(PetroBunk,null=True,blank=True)
    date = models.DateTimeField(null=True,blank=True)
    red_litre = models.PositiveIntegerField()
    green_litre = models.PositiveIntegerField()
    diesel_litre = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    veh_num = models.CharField(max_length=50, null=True, blank=True)
    added_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.bunk.name)

class ExpenseRecord(models.Model):
    bunk = models.ForeignKey(PetroBunk,null=True)
    date = models.DateField(null=True,blank=True,default=datetime.date.today)
    reason = models.CharField(null=True,blank=True,max_length=20)
    amount = models.DecimalField(max_digits=9, decimal_places=2,null=True,blank=True)
    receiver = models.CharField(null=True,blank=True,max_length=5)
    def __unicode__(self):
        return str(self.bunk)

class FuelRate(models.Model):
    red_rate = models.DecimalField(max_digits=9, decimal_places=2,null=True,blank=True)
    green_rate = models.DecimalField(max_digits=9, decimal_places=2,null=True,blank=True)
    diesel_rate = models.DecimalField(max_digits=9, decimal_places=2,null=True,blank=True)

    def __unicode__(self):
        return "%s-%s-%s" % (self.red_rate,self.green_rate,self.diesel_rate)

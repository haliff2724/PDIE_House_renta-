from django.db import models

# Create your models here.

class Admin(models.Model):
    staffid = models.CharField(max_length=20, primary_key=True)
    staffpass = models.CharField(max_length=100)

class Student(models.Model):
    studID = models.CharField(max_length=20, primary_key=True)
    studName = models.CharField(max_length=100)
    studPass = models.CharField(max_length=60)
    studGender = models.CharField(max_length=10)
    studNo = models.CharField(max_length=20)
    guardNo = models.CharField(max_length=20)
    studAddress = models.CharField(max_length=100)

class Landlord(models.Model): #driver register / prefix && login
    landID = models.CharField(max_length=20, primary_key=True)
    landName = models.CharField(max_length=100)
    landNo = models.CharField(max_length=20)
    landPass = models.CharField(max_length=100)

class Properties(models.Model): 
    propID =  models.CharField(max_length=7, primary_key=True) #if propID exist in Rental then will display not available
    propType = models.CharField(max_length=30)
    propSize = models.CharField(max_length=100)
    propPrice = models.DecimalField(max_digits=10, decimal_places=2)
    propLoc = models.CharField(max_length=30) 
    landID = models.ForeignKey(Landlord,on_delete=models.CASCADE)

class Rental(models.Model):
    propID = models.ForeignKey(Properties,on_delete=models.CASCADE) #tukar bookingid ke tripid
    studID = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(default='Pending', max_length=30)


class Service(models.Model):
    propID = models.ForeignKey(Properties, on_delete=models.CASCADE)
    studID = models.ForeignKey(Student, on_delete=models.CASCADE)
    details = models.CharField(max_length=100)  
    m_date = models.DateField(null=True , blank=True) # staff edit & view / driver views if they assign
    m_time = models.TimeField(null=True , blank=True)
    status = models.CharField(default='Pending' , max_length=30)


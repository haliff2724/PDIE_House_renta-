from django.contrib import admin
from .models import Admin, Student, Landlord, Properties, Service, Rental
# Register your models here.

admin.site.register(Admin)
admin.site.register(Student)
admin.site.register(Landlord)
admin.site.register(Properties)
admin.site.register(Service)
admin.site.register(Rental)
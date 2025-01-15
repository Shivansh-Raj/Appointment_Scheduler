from django.contrib import admin
from .models import Appointment, Availability, CustomUser
# Register your models here.

admin.site.register(Appointment)
admin.site.register(CustomUser)
admin.site.register(Availability)
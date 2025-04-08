from django.contrib import admin
from . models import Staff,Station,AvailableSlot,Booking
from user.models import Client
# Register your models here.
admin.site.register(Staff)
admin.site.register(AvailableSlot)
admin.site.register(Booking)
admin.site.register(Client)
admin.site.register(Station)
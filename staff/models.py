from django.db import models
from user.models import Client

# Create your models here.

class Staff(models.Model):
    staff=models.ForeignKey(Client,on_delete=models.CASCADE)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=15,blank=True,null=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return self.staff.username


class Station(models.Model):
    user=models.ForeignKey(Staff,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    location=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    quik_map=models.URLField()

    def __str__(self):
        return self.name
    
class AvailableSlot(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    name=models.CharField(max_length=150)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    is_booked = models.BooleanField(default=False)

class Booking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    slot = models.ForeignKey(AvailableSlot, on_delete=models.CASCADE)
    booked_at = models.DateTimeField()
    booking_date=models.DateField(null=True,blank=True)
    booking_time=models.TimeField(null=True,blank=True)

    def __str__(self):
        return f"{self.client.username} booked {self.slot}"


    
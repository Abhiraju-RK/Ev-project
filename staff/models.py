from django.db import models
from user.models import Client
from django.contrib.auth.models import User
# Create your models here.

class Staff(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=15,blank=True,null=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return self.user.username


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

    def is_available(self,booking_date,booking_time):
        return not Booking.objects.filter(
            slot__station=self.station,
            booking_date=booking_date,
            booking_time=booking_time,
        ).exists()

class Booking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    slot = models.ForeignKey(AvailableSlot, on_delete=models.CASCADE)
    booked_at = models.DateTimeField()
    booking_date=models.DateField(null=True,blank=True)
    booking_time=models.TimeField(null=True,blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)  # User can choose 30, 60, 90, etc.
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')

    def __str__(self):
        return f"{self.client.user.username} booked {self.slot}"


    
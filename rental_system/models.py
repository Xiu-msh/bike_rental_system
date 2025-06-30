from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    register_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Station(models.Model):
    station_name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.station_name

class Bicycle(models.Model):
    STATUS_CHOICES = [
        ('available', '可用'),
        ('rented', '已租'),
        ('maintenance', '维修中')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    station = models.ForeignKey(Station, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bicycle {self.id} at {self.station}"

class RentalRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE)
    rent_time = models.DateTimeField(auto_now_add=True)
    return_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} rented {self.bicycle}"

class MaintenanceRecord(models.Model):
    bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE)
    maintenance_date = models.DateField(auto_now_add=True)
    maintenance_description = models.TextField()

    def __str__(self):
        return f"Maintenance for {self.bicycle} on {self.maintenance_date}"
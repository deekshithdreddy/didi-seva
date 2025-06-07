
from django.db import models
from django.contrib.auth.models import User

class Maid(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    profile_pic = models.ImageField(upload_to='maid_profiles/', null=True, blank=True)
    services = models.CharField(max_length=255)
    experience = models.IntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)
    
    def __str__(self):
        return self.user.username

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    profile_pic = models.ImageField(upload_to='customer_profiles/', null=True, blank=True)
    
    def __str__(self):
        return self.user.username

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    SERVICE_CHOICES = [
        ('cleaning', 'House Cleaning'),
        ('cooking', 'Cooking'),
        ('childcare', 'Child Care'),
        ('eldercare', 'Elder Care'),
        ('laundry', 'Laundry'),
        ('fullday', 'Full Day Service'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    maid = models.ForeignKey(Maid, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    service_date = models.DateTimeField()
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES, default='cleaning')
    duration_hours = models.PositiveIntegerField(default=2)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"Booking #{self.id} - {self.customer.user.username} -> {self.maid.user.username}"

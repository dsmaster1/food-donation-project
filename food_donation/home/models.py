from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=300, null=True)
    profilepic = models.ImageField(upload_to='user', null=True, blank=True)
    register_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=300, null=True)
    profilepic = models.ImageField(upload_to='staff', null=True, blank=True)
    idpic = models.ImageField(upload_to='staff', null=True)
    about = models.CharField(max_length=300, null=True)
    status = models.CharField(max_length=20, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=300, null=True)
    register_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100, null=True)
    item_pic = models.ImageField(upload_to='donation', null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=300, null=True)
    donation_date = models.DateField(null=True)
    last_update = models.DateField(null=True)
    admin_remark = models.CharField(max_length=200, null=True)
    staffremark = models.CharField(max_length=200, null=True)
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, null=True) 
    status = models.CharField(max_length=30, null=True) 
    reached_location = models.BooleanField(default=False)      

    def __str__(self):
        return f"{self.item_name} donated by {self.donor.user.username}"
    
    @property
    def is_booked(self):
    
        return self.bookings.exists()
    
class Booking(models.Model):
    donation = models.ForeignKey(Donation,on_delete=models.CASCADE,related_name="bookings")
    booked_by = models.ForeignKey(Donor, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donation.item_name} booked by {self.booked_by.user.username}"



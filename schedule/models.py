from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.contrib.auth.models import CustomUser

class CustomUser(AbstractUser):
    is_Professor = models.BooleanField(default=False)
    is_Student = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class Availability(models.Model):
    # Suppose if we don't include limit_choices_to, the dropdown will show all users i.e. both professors and students, which might lead to incorrect assignments (e.g., setting a student as a professor).
    Professor_id= models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_Professor':True})
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    isBooked = models.BooleanField(default=False)


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Booked', 'Booked'),
        ('Cancelled', 'Cancelled'),
    ]
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_Student': True})
    professor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='professor_appointments', limit_choices_to={'is_Professor': True})
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Booked')
    created_at = models.DateTimeField(auto_now_add=True)


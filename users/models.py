from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser): 
    email = models.EmailField(unique=True)
    followed_events = models.ManyToManyField('organizers.Event', related_name='followers', blank=True)


    # ทำให้เห็นใน หน้า admin
    def __str__(self):
        return self.username
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    # Organizer: is_staff = True
    def is_organizer(self):
        return self.is_staff

    # Customer: is_staff = False
    def is_customer(self):
        return not self.is_staff  

class UserProfile(models.Model):
    class Gender(models.Choices):
        M = "M"
        F = "F"
        Other = "Other"

    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)  
    profile_picture = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class EventParticipant(models.Model):
    class RegisterStatus(models.Choices):
        Register = "Register"
        Attended = "Attended"
        Cancelled = "Cancelled"
        No_Show = "No Show"

    event = models.ForeignKey("organizers.Event", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    participation_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=30,
        choices=RegisterStatus.choices,  
        default=RegisterStatus.No_Show
    )

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"


class Ticket(models.Model):
    class StatusChoices(models.TextChoices):
        Valid = 'Valid'
        Used = 'Used'
        Expired = 'Expired'

    event_participant = models.OneToOneField("users.EventParticipant", on_delete=models.CASCADE)
    qr_code = models.CharField(max_length=255)
    qr_code_image = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    status = models.CharField(
        max_length=15,
        choices=StatusChoices.choices,  
        default=StatusChoices.Valid  
    )
    issue_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"Ticket for {self.event_participant.user.username} - {self.event_participant.event }"





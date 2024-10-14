from django.db import models
from django.contrib.auth.models import AbstractUser

import random
import string


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
        M = 'M'
        F = 'F'
        Other = 'Other'

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)  
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) 

    def __str__(self):
        return self.user.username

class EventParticipant(models.Model):
    class RegisterStatus(models.Choices):
        Register = 'Register'
        Attended = 'Attended'
        Cancelled = 'Cancelled'
        No_Show = 'No Show'

    event = models.ForeignKey('organizers.Event', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
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
        

    event_participant = models.OneToOneField('users.EventParticipant', on_delete=models.CASCADE)
    qr_code = models.CharField(max_length=255, null=True, blank=True)
    qr_code_image = models.URLField(null=True, blank=True)
    status = models.CharField(
        max_length=15,
        choices=StatusChoices.choices,  
        default=StatusChoices.Valid
    )
    issue_date = models.DateField(auto_now_add=True)
    # แก้ข้อมูลไม่ได้
    entry_code = models.CharField(max_length=10, unique=True, editable=False)

    # *args สำหรับ positional arguments ไม่มีชื่อ **kwargs สำหรับ keyword arguments ex.entry_code=123
    # save คือ ของดั้งเดิมของ django (เราแค่ทำการ override มัน)
    # https://www.geeksforgeeks.org/overriding-the-save-method-django-models/
    def save(self, *args, **kwargs):
        # ดูว่า entry_code ใน model ว่างไหม ถ้าก็จะสร้างขึ้นมา 
        if not self.entry_code:
            # entry_code ยังไม่มี จะเรียก generate_entry_code เพื่อสร้างรหัสเข้าใหม่ เองทันที
            self.entry_code = self.generate_entry_code()
        # เพื่อขยายการทำงานของ method save ยังคง method save แบบของ Django ไว้  
        super().save(*args, **kwargs)

    def generate_entry_code(self):
        # สุ่ม A-Z 6 ตัว
        letters = ''.join(random.choices(string.ascii_uppercase, k=6))
        # สุ่ม 0-9 4 ตัว
        digits = ''.join(random.choices(string.digits, k=4))
        return letters + digits

    def __str__(self):
        return f"Ticket for {self.event_participant.user.username} - {self.event_participant.event }"





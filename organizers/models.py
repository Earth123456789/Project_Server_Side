from django.db import models
from django.utils.html import mark_safe

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    # ทำให้เห็นใน หน้า admin
    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True ,null=True)
    email = models.EmailField(unique=True ,blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    contact = models.URLField(max_length=200, blank=True, null=True)

     # ทำให้เห็นใน หน้า admin
    def __str__(self):
        return self.name
    

class Location(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

     # ทำให้เห็นใน หน้า admin
    def __str__(self):
        return self.name

class Event(models.Model):
    class EventStatus(models.Choices):
        Show = 'Show'
        Close = 'Close'
        Past = 'Past'


    location = models.ForeignKey("organizers.Location", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True ,null=True)
    start_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    image = models.ImageField(upload_to='event_images/')  
    max_participants = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category)
    company = models.ForeignKey(Company, on_delete=models.CASCADE) 
    status = models.CharField(max_length=10, choices=EventStatus.choices, default='Show')
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)   # ราคาต่อใบ

     # ทำให้เห็นใน หน้า admin
    def __str__(self):
        return self.name
    
    def is_one_day_event(self):
        return self.start_date.date() == self.end_date.date()
    
    def is_full(self):
        return self.eventparticipant_set.count() >= self.max_participants

class Payment(models.Model):
    class PaymentStatus(models.Choices):
        Verification = 'Verification'
        Successful = 'Successful'
        Failed  = 'Failed'

    event = models.ForeignKey("organizers.Event", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    ticket_quantity = models.PositiveIntegerField(default=1)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # ราคารวม
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=PaymentStatus, default='Verification')
    cancel_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Payment by {self.user} for {self.event} - {self.amount}"
    
    


    


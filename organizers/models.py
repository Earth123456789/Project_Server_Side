from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

class Company(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True ,null=True)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, null=True)
    contact = models.URLField(max_length=200)
    

class Location(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ManyToManyField(Category)

class Event(models.Model):
    location = models.OneToOneField("organizers.Location", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True ,null=True)
    start_date = models.DateTimeField() 
    end_date = models.DateTimeField(blank=True, null=True) 
    image = models.ImageField(upload_to='event_images/')  
    max_participants = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category)
    company = models.ForeignKey(Company, on_delete=models.CASCADE) 

    def __str__(self):
        return self.event_name
    
    def is_one_day_event(self):
        return self.start_date.date() == self.end_date.date()
    
    def is_full(self):
        return self.eventparticipant_set.count() >= self.max_participants
    


    


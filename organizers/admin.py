from django.contrib import admin
from .models import Category, Company, Location, Event, Payment
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'telephone', 'contact')  

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'start_date', 'start_time', 'end_date', 'end_time', 'company', 'get_categories', 'image')  

    # ใช้ for loop เพราะ เป็น Many to Many
    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()])
    # ทำให้ ชื่อตรง list_display ขึ้นเป็น Categories
    get_categories.short_description = 'Categories' 

@admin.register(Payment)
class EventAdmin(admin.ModelAdmin):
    list_display = ('company', 'event' , 'user', 'ticket_quantity', 'amount', 'status', 'payment_date')  

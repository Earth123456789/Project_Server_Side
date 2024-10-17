from django import template

# เก็บ instance ของ template.Library
register = template.Library()

# ฟังก์ชันเป็น filter ใหม่ที่ใช่ใน template ได้
@register.filter
def custom_date(start_date, end_date):
    if start_date and end_date:
        return f"{start_date.strftime('%d')} - {end_date.strftime('%d %b %Y')}"
    return f"{start_date.strftime('%d %b %Y')}"

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from organizers.models import Event
# Create your views here.
class HomepageView(View):
    def get(self, request):
        # Query ข้อมูล Event ที่มีรูปภาพ
        events_with_images = Event.objects.exclude(image='')  # ดึงเฉพาะ event ที่มีรูปภาพ

        # ส่งข้อมูลไปยังเทมเพลต
        return render(request, 'homepage.html', {'events': events_with_images})
    
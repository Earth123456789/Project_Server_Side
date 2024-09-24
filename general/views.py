from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from organizers.models import Event, Category
from django.db.models import Count
# Create your views here.

class HomepageView(View):
    def get(self, request):

        # รับค่าหมวดหมู่จาก query parameters แทน session
        category_name = request.GET.get('category', None)

        # ดึง Event ตามหมวดหมู่ที่ระบุ
        if category_name:
            events = Event.objects.filter(category__name=category_name)
        else:
            events = Event.objects.all()


        # ดึง Event ที่มีผู้ติดตามมากที่สุด โดยดึงผ่าน related_name='followers'  
        # cardfollowers.html
        most_followed_event = Event.objects.annotate(num_followers = Count('followers')).order_by('-num_followers')[:3]

        # silder.html
        slider_events = Event.objects.all()[:5]

        # homepage.html
        categories = Category.objects.all()

        context = {
            "events" : events,
            "slider_events": slider_events, 
            "most_followed_event" : most_followed_event,
            "categories": categories,
            "selected_category": category_name,
        }

        return render(request, 'general/homepage.html', context)
    
    
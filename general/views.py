from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.db.models import Count
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from users.models import UserProfile, User

from organizers.models import Event, Category, Company

# Create your views here.

class HomepageView(View):
    def get(self, request):

        # รับค่าหมวดหมู่จาก query parameters (get ค่าจาก name="category" ใน template)
        category_name = request.GET.get('category', None)

        search = request.GET.get('search', None)

        current_time = timezone.now() 

        event_filter = Q(end_date__gte=current_time) | Q(end_date__isnull=True, start_date__gte=current_time)

        # ดึง Event ตามหมวดหมู่ที่ระบุ
        if category_name:
            events = Event.objects.filter(category__name=category_name).filter(event_filter)
        else:
            events = Event.objects.filter(event_filter)
        
        if search:
            # คืนค่าทุกเหตุการณ์ไม่ว่าจะเป็นตัวพิมพ์ใหญ่หรือตัวพิมพ์เล็ก
            events = Event.objects.filter(name__icontains=search).filter(event_filter)

        
        has_company = False
        company = None
        if request.user.is_authenticated:
            # ตรวจสอบว่าผู้ใช้ มี Company ไหม
            try:
                company = Company.objects.get(user=request.user)
                has_company = True
            except Company.DoesNotExist:
                has_company = False
            


        # ดึง Event ที่มีผู้ติดตามมากที่สุด โดยดึงผ่าน related_name='followers'  
        # cardfollowers.html
        # silder.html
        most_followed_event = None
        slider_events = None
        if not search:
            most_followed_event = Event.objects.annotate(num_followers=Count('followers')).filter(end_date__gte=current_time).order_by('-num_followers')[:3]
            slider_events = Event.objects.filter(end_date__gte=current_time)[:5]
    
        # homepage.html
        categories = Category.objects.all()
        

        context = {
            "events" : events,
            "slider_events": slider_events, 
            "most_followed_event" : most_followed_event,
            "categories": categories,
            "selected_category": category_name,
            "has_company": has_company,
            "company": company,
        }

        return render(request, 'general/homepage.html', context)
    
class EventView(View):
     

    def get(self, request, event_id):

        has_company = False
        company = None
        if request.user.is_authenticated:
            # ตรวจสอบว่าผู้ใช้ มี Company ไหม
            try:
                company = Company.objects.get(user=request.user)
                has_company = True
            except Company.DoesNotExist:
                has_company = False
         
        event = Event.objects.get(pk=event_id)
        context = {
            "event" : event,
            "has_company": has_company,
            "company": company,
        }

        return render(request, "general/event_detail.html", context)
    
    def put(self, request, event_id, user_id):
        event = Event.objects.get(pk = event_id)
        user = User.objects.get(pk = user_id)
        user.followed_events.add(event)
        return JsonResponse({'status':'add_susecss'}, status=200)
    
    def delete(self, request,  event_id, user_id):
        event = Event.objects.get(pk = event_id)
        user = User.objects.get(pk = user_id)
        user.followed_events.remove(event)
        return JsonResponse({'status':'remove_susecss'}, status=200)




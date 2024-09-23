from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from organizers.models import Event, Category
from django.db.models import Count
# Create your views here.

class HomepageView(View):
    def get(self, request):

        # รับค่าหมวดหมู่จาก session (ถ้า POST ถูกใช้ก่อนหน้า) (get() จะพยายามดึงค่าของคีย์ 'category' จาก session ถ้าค่ามีอยู่ใน session มันจะถูกเก็บไว้ในตัวแปร category_name. ถ้าค่ามีไม่อยู่ (category ไม่ถูกตั้งค่าใน session), จะคืนค่า None แทน. )
        category_name = request.session.get('category', None)

        # เกี่ยว session
        if category_name:
            # card.html + homepage.html
            events = Event.objects.filter(category__name=category_name)
        else:
            # card.html
            events = Event.objects.all()

        # ไม่เกี่ยวกับ session ดึง DB ธรรมดา

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
    
    def post(self, request):
        
        # เก็บหมวดหมู่ใน session แล้ว redirect กลับไปที่หน้าเดิม
        category_name = request.POST.get('category')
        request.session['category'] = category_name
        return redirect('homepage')
    
    
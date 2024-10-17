from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.db.models import Count
from django.utils import timezone
from django.db.models import Q
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import UserProfile, User

from organizers.models import Event, Category, Company

import google.generativeai as genai


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

        organizer = request.user.groups.filter(name='Organizers').exists()

        context = {
            "events" : events,
            "slider_events": slider_events, 
            "most_followed_event" : most_followed_event,
            "categories": categories,
            "selected_category": category_name,
            "has_company": has_company,
            "company": company,
            "organizer": organizer
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

        # ตรวจสอบว่ากิจกรรมใกล้จะถึงภายใน 3 วัน
        # timedelta ใช้เปรียบเทียบระยะเวลา
        if event.start_date - timezone.now().date() <= timedelta(days=3):
            self.send_email(user, event)

        return JsonResponse({'status':'add_susecss'}, status=200)
    
    def delete(self, request,  event_id, user_id):
        event = Event.objects.get(pk = event_id)
        user = User.objects.get(pk = user_id)
        user.followed_events.remove(event)
        return JsonResponse({'status':'remove_susecss'}, status=200)
    
    def send_email(self, user, event):
        subject = 'ใกล้ถึงเวลาแล้ว!!!!'

        # render template เป็น string โดยไม่ต้องส่ง response
        message = render_to_string('users/event_reminder_email.html', {
            'user': user,
            'event': event,
        })

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        email = EmailMessage(subject, message, from_email, recipient_list)
        email.content_subtype = 'html'
        email.send()

class ChatView(LoginRequiredMixin, View):
   login_url = 'login'

   def get(self, request, user_id):
        
        if request.user.is_authenticated:
            # ตรวจสอบว่าผู้ใช้ มี Company ไหม
            try:
                company = Company.objects.get(user=request.user)
                has_company = True
            except Company.DoesNotExist:
                has_company = False
        
        if request.user.id != user_id:
            raise PermissionDenied("เข้าได้เฉพาะผู้ใช้งานที่กำหนดไว้")
        
        context = {
            "has_company": has_company,
            "company": company,
        }
        
        return render(request, "general/chat.html", context)

class ChatBotView(APIView):

    def post(self, request):
        # รับข้อความจากผู้ใช้
        user_input = request.data.get('message')

        if not user_input:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # ตั้งค่า API Key ของ Google
            genai.configure(api_key=settings.GOOGLE_API_KEY)

            # คำแนะนำสำหรับหมวดหมู่อีเวนต์
            word_recommendation = ["แนะนำอีเวนต์", "Event Recommend", "แนะนำอะไรสนุกๆหน่อย", "ขออะไรสนุกๆ"]
            word_category_sport = ["แนะนำอีเวนต์กีฬาหน่อย", "กีฬา", "อยากหาไรสนุกๆ", "แนะนำอะไรสนุกๆหน่อย", "ขออะไรสนุกๆ"]
            word_category_entertain = ["แนะนำอีเวนต์ที่สนุกๆหน่อย", "บันเทิง", "สนุก", "แนะนำอะไรสนุกๆหน่อย", "ขออะไรสนุกๆ"]
            word_category_learn = ["แนะนำอีเวนต์ที่ได้ความรู้หน่อย", "ความรู้", "การเรียนรู้"]
            word_category_lifestyle = ["แนะนำอีเวนต์ที่เกี่ยวชีวิตประจำวันหน่อย", "ชีวิตประจำวัน", "lifestyle"]

            # ตรวจสอบข้อความที่ผู้ใช้ป้vpkอนเข้ามาและกรองอีเวนต์ตามหมวดหมู่
            if any(keyword in user_input.lower() for keyword in word_category_sport):
                # กรองอีเวนต์หมวดกีฬา
                events = Event.objects.filter(category__name='กีฬา')
                category = "กีฬา"
            elif any(keyword in user_input.lower() for keyword in word_category_entertain):
                # กรองอีเวนต์หมวดบันเทิง
                events = Event.objects.filter(category__name='บันเทิง')
                category = "บันเทิง"
            elif any(keyword in user_input.lower() for keyword in word_category_learn):
                # กรองอีเวนต์หมวดการเรียนรู้
                events = Event.objects.filter(category__name='เรียนรู้')
                category = "เรียนรู้"
            elif any(keyword in user_input.lower() for keyword in word_category_lifestyle):
                # กรองอีเวนต์หมวดชีวิตประจำวัน
                events = Event.objects.filter(category__name='ไลฟ์สไตล์')
                category = "ไลฟ์สไตล์"
            elif any(keyword in user_input.lower() for keyword in word_recommendation):
                # กรองอีเวนต์ทั้งหมด
                events = Event.objects.all()
                category = "ทั้งหมด"
            else:
                # ถ้าข้อความไม่เกี่ยวข้องกับ Event ให้ใช้ Google Generative AI
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(user_input)
                bot_response = response.text
                return Response({"message": bot_response}, status=status.HTTP_200_OK)

            # สร้างข้อความแนะนำ Event
            if events.exists():
                recommendations = [f"กิจกรรม: {event.name}" for event in events]
                bot_response = f"กิจกรรม {category}:" + " ".join(recommendations)
            else:
                bot_response = f"ไม่มีข้อมูลกิจกรรมในหมวดหมู่ {category} ขณะนี้"

            return Response({"message": bot_response}, status=status.HTTP_200_OK)

        except Exception as server_error:
            return Response({"error": str(server_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
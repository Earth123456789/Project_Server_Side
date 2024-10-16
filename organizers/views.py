from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import Group
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from organizers.forms import CompanyRegistrationForm
from organizers.models import Company, Payment, Event

from users.models import User, EventParticipant, Ticket

import json

class OrganizerRegisterView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        form = CompanyRegistrationForm()

        user = request.user

        # ตรวจว่า Company อยู่แล้วไหม
        if Company.objects.filter(user=user).exists():
            return redirect('dashboard')  
        
        # หากผู้ใช้ยังไม่ได้เข้าสู่ระบบ 
        if user.is_anonymous:
            return redirect('login')
        
        context = {
            'form': form
        }
        return render(request, 'registration/organizer.html', context)
    
    @transaction.atomic
    def post(self, request):
        # ดึงข้อมูลผู้ใช้จาก request
        user = request.user

        form = CompanyRegistrationForm(request.POST)

        if form.is_valid():
            # Create, but don't save the company instance. (ทำเพื่อติดตามว่าใครสร้างหรือเชื่อมโยงกับ Company)
            # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method
            company = form.save(commit=False)  
            company.user = user  
            # Now, save the data for the form.
            company.save()  

            # เพิ่มผู้ใช้ในกลุ่ม "Organizers"
            organizer_group, created = Group.objects.get_or_create(name='Organizers')
            user.groups.add(organizer_group)

            return redirect('homepage')  

        context = {
            'form': form
        }
        return render(request, 'registration/organizer.html', context)

class DashBoardView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, company_id):
        user = request.user

        company = Company.objects.get(pk=company_id)

        event_count = Event.objects.filter(company=company_id).count()

        transaction_count = Payment.objects.filter(company=company_id).count()
        
        event_participant_count = EventParticipant.objects.filter(event__company=company).values('event__name').annotate(participant_count=Count('id'))

        # ตาม week 4-5 เลยคร๊าบ
        event_names = [event['event__name'] for event in event_participant_count]
        participant_counts = [event['participant_count'] for event in event_participant_count]

        print(event_participant_count)
        print(event_names)
        print(participant_counts)


        # ตรวจสอบว่าเป็น "Organizers"
        if not user.groups.filter(name='Organizers').exists():
            raise PermissionDenied("เข้าได้เฉพาะผู้ใช้งานที่กำหนดไว้")
        
        # ไม่ได้ลงทะเบียนเป็นบริษัท
        if not Company.objects.filter(user=user).exists():
            return redirect('organizer-register')  
        
        # เจ้าของบริษัทจริงๆ
        if company.user != user:
            raise PermissionDenied("เข้าได้เฉพาะเจ้าของบริษัทเท่านั้น")

        # ไม่ได้เข้าสู่ระบบ 
        if user.is_anonymous:
            return redirect('login')

        context = {
            "company": company,
            "event": event_count,
            "transaction": transaction_count,
            "event_names": event_names,  
            "participant_counts": participant_counts, 
        }
        return render(request, 'organizers/dashboard.html', context)  
    

class TransactionView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, company_id):
        user = request.user

        company = Company.objects.get(pk=company_id)

        transactions = Payment.objects.filter(company=company_id).order_by("-status", "payment_date")

        print(transactions)


        # ตรวจสอบว่าเป็น "Organizers"
        if not user.groups.filter(name='Organizers').exists():
            raise PermissionDenied("เข้าได้เฉพาะผู้ใช้งานที่กำหนดไว้")
        
        # ไม่ได้ลงทะเบียนเป็นบริษัท
        if not Company.objects.filter(user=user).exists():
            return redirect('organizer-register')  
        
        # เจ้าของบริษัทจริงๆ
        if company.user != user:
            raise PermissionDenied("เข้าได้เฉพาะเจ้าของบริษัทเท่านั้น")

        # ไม่ได้เข้าสู่ระบบ 
        if user.is_anonymous:
            return redirect('login')
        
        print(transactions)
        context = {
            "company": company,
            "transactions": transactions
        }
        return render(request, 'organizers/transaction.html', context)  
    
    def post(self, request, company_id):
        transaction_id = request.POST.get('transaction_id')  
        transaction = Payment.objects.get(pk=transaction_id)

        # เปลี่ยนสถานะ
        if transaction.status == "Verification":
            transaction.status = "Successful"
            transaction.save()
        
        # ส่งอีเมลยืนยันการเข้าร่วมงาน
        # ส่งให้ตาม transaction.user และ ดู event ที่ transaction.event.id
        self.send_email(transaction.user, transaction.event.id, request)

        return redirect('transaction', company_id=company_id)  
    
    def send_email(self, user, event_id, request):

        subject = 'ยืนยันการเข้าร่วมงาน'
        
        # ดึง domain จาก request
        domain = request.get_host()

        # สร้าง token และ uid เพื่อใช้ในการสร้างลิงก์ยืนยัน
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # สร้างลิงก์ยืนยันการเข้าร่วมงาน โดยใช้ event_id
        link = f'http://{domain}/user/event/success/{event_id}/{uid}/{token}/'

        # ใช้ template อีเมลเพื่อสร้างข้อความอีเมล
        message = render_to_string('users/email_ticket.html', {
            'user': user,
            'event_id': event_id,
            'link': link,
        })

        # กำหนดข้อมูลการส่งอีเมล
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        # ส่งอีเมล
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.send()

class CancelTransactionView(View):
    def post(self, request, company_id):

        # เอาข้อมูลที่ user
        #  body: JSON.stringify({ 'transaction_id': transactionId, 'cancel_text': result.value  })
        data = json.loads(request.body)
        transaction_id = data.get('transaction_id')
        cancel_text = data.get('cancel_text')

        print(transaction_id)
        print(cancel_text)

        # ตรวจสอบว่าได้ transaction_id หรือไม่
        if not transaction_id:
            return JsonResponse({'success': False, 'message': 'ไม่มี transaction_id'}, status=404)

        # ดึง Payment object จาก transaction_id
        transaction = Payment.objects.get(pk=transaction_id)

        # ถ้ามีเหตุผลการยกเลิก ให้เปลี่ยนสถานะเป็น "Failed"
        if transaction.status == "Verification":
            if cancel_text:
                transaction.status = "Failed"
                transaction.cancel_text = cancel_text
                transaction.save()
            return JsonResponse({'success': True, 'message': 'ยกเลิกรายการสำเร็จ'}, status=200)
        else:
            return JsonResponse({'success': False, 'message': 'ไม่มีเหตุผลการยกเลิก'}, status=404)
    
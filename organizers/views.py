from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import Group
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from organizers.forms import CompanyRegistrationForm
from organizers.models import Company

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

        # ตรวจสอบว่าเป็น "Organizers"
        if not user.groups.filter(name='Organizers').exists():
            raise PermissionDenied("เข้าได้เฉพาะผู้ใช้งานที่กำหนดไว้")

        if not Company.objects.filter(user=user).exists():
            return redirect('organizer-register')  

        # ไม่ได้เข้าสู่ระบบ 
        if user.is_anonymous:
            return redirect('login')

        context = {
            "company": company
        }
        return render(request, 'organizers/dashboard.html', context)  # เปลี่ยนไปที่หน้าแดชบอร์ดที่คุณต้องการแสดง
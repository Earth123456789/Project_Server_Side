# users/views.py 
from django.shortcuts import render, redirect
from django.views import View
from users.forms import UserRegistrationForm, UserLoginForm
from django.db import transaction
from users.models import UserProfile
from django.contrib.auth import logout, login

# Create your views here.
class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})
    
    # จัดการข้อผิดพลาด ทำให้ไม่ต้องทำความสะอาดฐานข้อมูลด้วยตัวเอง บันทึกข้อมูลในครั้งเดียวแทนที่จะบันทึกทีละรายการ
    @transaction.atomic
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # แฮชรหัสผ่าน
            user.set_password(form.cleaned_data['password']) 
            user.save()

            # บันทึกข้อมูลโปรไฟล์
            user_profile = UserProfile(
                user=user,
                gender=form.cleaned_data['gender'], # ระดับ filed
                telephone=form.cleaned_data['telephone'],
                date_of_birth=form.cleaned_data['date_of_birth'],
            )
            user_profile.save()

            return redirect('login')

        return render(request, 'registration/register.html', {'form': form})
    

class LoginView(View):
    
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'registration/login.html', {"form": form})
    
    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            # backends.py (มีการแก้เพิ่ม)
            user = form.get_user() 
            # login + สร้าง session
            login(request,user)
            
            return redirect('homepage')  
        print(form.errors)
        return render(request,'registration/login.html', {"form":form})

class LogoutView(View):
    
    def get(self, request):
        logout(request)
        return redirect('homepage')

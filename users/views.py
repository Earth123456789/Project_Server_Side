# users/views.py 
from django.shortcuts import render, redirect
from django.views import View
from users.forms import UserRegistrationForm, UserLoginForm, ChangePasswordForm
from django.db import transaction
from users.models import UserProfile, User
from django.contrib.auth import logout, login
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse


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
            print(user) # test  
            # login + สร้าง session
            login(request,user)
            
            return redirect('homepage')  
        
        print(form.errors)
        return render(request,'registration/login.html', {"form":form})

class LogoutView(View):
    
    def get(self, request):
        logout(request)
        return redirect('homepage')
    
class ChangePasswordView(View):

    def get(self, request):
        form = ChangePasswordForm()
        return render(request, 'registration/change_password_form.html', {'form': form})
    
    def post(self, request):
        form = ChangePasswordForm(data=request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            # ส่งอีเมลยืนยันการเปลี่ยนรหัสผ่าน
            self.send_email(user)
            messages.success(request, 'เช็คอีเมลของคุณเพื่อทำการเปลี่ยนรหัสผ่าน')
            return redirect('login')
        
        print(form.errors)
        return render(request, 'registration/change_password_form.html', {'form': form})

    def send_email(self, user):
        subject = 'การเปลี่ยนรหัสผ่าน'
        message = f'สวัสดี {user.username},\n\nคุณได้เปลี่ยนรหัสผ่านของคุณเรียบร้อยแล้ว หากคุณไม่ได้ทำการเปลี่ยนแปลงนี้ กรุณาติดต่อเราที่ support@example.com'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        email = EmailMessage(subject, message, from_email, recipient_list)
        email.send()




# users/views.py 
from django.shortcuts import render, redirect
from django.views import View
from django.db import transaction
from django.contrib.auth import logout, login
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse

from users.forms import UserRegistrationForm, UserLoginForm, ChangePasswordForm, UserPasswordChangeForm, AttendeeForm, UserProfileForm
from users.models import UserProfile, User, EventParticipant, Ticket

from organizers.models import Event


# register.html, login.html, forms.py, models.py
class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()

        context = {
            'form': form
        }

        return render(request, 'registration/register.html', context)
    
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
        
        context = {
            'form': form
        }

        return render(request, 'registration/register.html', context)
    
# register.html, login.html, forms.py, backends.py, signals.py, models.py
class LoginView(View):
    
    def get(self, request):
        form = UserLoginForm()

        context = {
            "form": form
        }

        return render(request, 'registration/login.html', context)
    
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

        context = {
            'form': form
        }

        return render(request,'registration/login.html', context)

class LogoutView(View):
    
    def get(self, request):
        logout(request)
        return redirect('homepage')

# change_password_form.html, forms.py, password_reset_email.html , models.py 
class ChangePasswordView(View):

    def get(self, request):
        form = ChangePasswordForm()

        context = {
            'form': form
        }

        return render(request, 'registration/change_password_form.html', context)
    
    def post(self, request):
        form = ChangePasswordForm(data=request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            # ส่งอีเมลยืนยันการเปลี่ยนรหัสผ่าน
            self.send_email(user, request)
            return redirect('login')
        
        print(form.errors)

        context = {
            'form': form
        }

        return render(request, 'registration/change_password_form.html', context)

    def send_email(self, user, request):
        
        subject = 'เปลี่ยนรหัสผ่าน'

        # ดึง domain จาก request
        domain = request.get_host()
        # สร้าง token ที่ไม่ซ้ำกันสำหรับผู้ใช้ (เป็นของ django)
        token = default_token_generator.make_token(user)
        # เข้ารหัส Primary Key ของผู้ใช้ให้ปลอดภัย (แบบ BASE 64)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        link = f'http://{domain}/user/password_reset_confirm/{uid}/{token}/'
        reset_link = f"{link}"

        # render template เป็น string โดยไม่ต้องส่ง response
        message = render_to_string('users/password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]


        email = EmailMessage(subject, message, from_email, recipient_list)
        email.send()


# password_reset_form.html, forms.py, models.py
class PasswordResetConfirmView(View):

    def get(self, request, uidb64, token):
        # ถอดรหัสข้อมูล เพื่อดึงข้อมูล User มาใช้งาน ถอดรหัสจะเป็น (user.pk) ที่ส่ง request เข้ามา
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        form = UserPasswordChangeForm(user)
        print(user)

        context = {
            'form': form,
            'valid_token': True
        }

        return render(request, 'users/password_reset_form.html', context)
    
    def post(self, request, uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        form = UserPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()  
            return redirect('login')
        else:

            context = {
                'form': form,
                'valid_token': True
            }

            return render(request, 'users/password_reset_form.html', context)

# receive.html, models.py
class ReceiveTicketView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, event_id):
        
        event = Event.objects.get(pk=event_id)
        context = {
            'event' : event
        }

        return render(request, "users/receive.html", context)
    
    def post(self, request, event_id):
        user = request.user
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        return redirect('attendent', event_id=event_id, uidb64=uid, token=token)

class AttendeeView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, event_id, uidb64, token):
        # ถอดรหัสข้อมูล 
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            user_profile = None
            
   
        form = AttendeeForm(instance=user)
        # ตั้งค่าค่าเริ่มต้น field ให้ใส่ userprofile ได้
        if user_profile:
            form.fields['telephone'].initial = user_profile.telephone
            form.fields['date_of_birth'].initial = user_profile.date_of_birth.strftime('%Y-%m-%d')
        else:
            form.fields['telephone'].initial = ''
            form.fields['date_of_birth'].initial = ''

        print(user_profile.date_of_birth)
        context = {
        'user': user,
        'valid_token': True,
        'form': form
        }
        print(user)
        return render(request, 'users/attendee.html', context)
        
    # จัดการข้อผิดพลาด ทำให้ไม่ต้องทำความสะอาดฐานข้อมูลด้วยตัวเอง บันทึกข้อมูลในครั้งเดียวแทนที่จะบันทึกทีละรายการ
    @transaction.atomic
    def post(self, request, event_id, uidb64, token):
        # ถอดรหัสข้อมูล 
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        event = Event.objects.get(pk=event_id)
        form = AttendeeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            
            user_profile = UserProfile.objects.get(user=user)

            user_profile.telephone = form.cleaned_data.get('telephone')  
            user_profile.date_of_birth = form.cleaned_data.get('date_of_birth')
            user_profile.gender = form.cleaned_data.get('gender')
            user_profile.save()
            participation = EventParticipant(
                user=user,
                event=event,
                status="Attended" 
            )
            participation.save()

            context = {
                'user': user,
                'valid_token': True,
                'form': form
            }
            print(user)
            print(form.errors)

            if event.ticket_price == 0.00:
                request_user = request.user
                token = default_token_generator.make_token(request_user)
                uid = urlsafe_base64_encode(force_bytes(request_user.pk))
                return redirect('success', event_id=event_id, uidb64=uid, token=token)
            else:
                return redirect('payment', event_id=event_id)
        
        context = {
            'user': user,
            'valid_token': True,
            'form': form
        }

        return render(request, 'users/attendee.html', context)

# ถ้าทำอันอื่นเสร็จเดี๋ยวกลับมาทำ
# class PaymentView(LoginRequiredMixin, View):
#     login_url = 'login'

#     def get(self, request, event_id):

#         user = request.user
         
#         is_registered = EventParticipant.objects.filter(user=user, event_id=event_id).exists()

#         if not is_registered:
#             return redirect('attendent', event_id=event_id, uidb64=urlsafe_base64_encode(force_bytes(user.pk)), token=default_token_generator.make_token(user))
        
#         return render(request, 'users/payment.html', {'event_id': event_id})


class SuccessView(View):

    def get(self, request, event_id, uidb64, token):
        # ถอดรหัสข้อมูล 
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        context = {
            'user': user
        }
        return render(request, 'users/success.html', context)
    
    # จัดการข้อผิดพลาด ทำให้ไม่ต้องทำความสะอาดฐานข้อมูลด้วยตัวเอง บันทึกข้อมูลในครั้งเดียวแทนที่จะบันทึกทีละรายการ
    @transaction.atomic
    def post(self, request, event_id, uidb64, token):
        # ถอดรหัสข้อมูล 
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        event_participants = EventParticipant.objects.filter(event_id=event_id, user=user)

        for event_participant in event_participants:
            event_participant.status = 'Register'
            event_participant.save() 


        ticket = Ticket(
            event_participant=event_participant,
        )
        qr_data = ticket.entry_code  
        qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?data={qr_data}&size=300x300"
        ticket.qr_code = qr_data
        ticket.qr_code_image = qr_code_url
        ticket.save()

        return redirect('homepage')
    
class UserProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, user_id):

        user = User.objects.get(pk=user_id)
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            user_profile = None

        form = UserProfileForm(instance=user) 
        
        if user_profile:
            form.fields['gender'].initial = user_profile.gender
            form.fields['telephone'].initial = user_profile.telephone
            form.fields['date_of_birth'].initial = user_profile.date_of_birth.strftime('%Y-%m-%d')
        else:
            form.fields['telephone'].initial = ''
            form.fields['date_of_birth'].initial = ''
        
        context = {
            'user': user,
            'form': form
        }

        return render(request, 'users/userprofile.html', context)
    
    def post(self, request, user_id):

        user = User.objects.get(pk=user_id)
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            user_profile = None

        # ต้องใช้ enctype="multipart/form-data" (กำหนดชนิดการเข้ารหัส เพื่อให้ sever file ที่เข้ามา)  file จะถูกผ่าน request.FILES
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

            user_profile.profile_picture = request.FILES['profile_picture']
            user_profile.gender = form.cleaned_data.get('gender')
            user_profile.telephone = form.cleaned_data.get('telephone')
            user_profile.date_of_birth = form.cleaned_data.get('date_of_birth')
            user_profile.save()

            return redirect('userprofile', user.id)
        else:
            
            context = {
                'user': user,
                'form': form
            }
            
            return render(request, 'users/userprofile.html', context)
    
class UserChangePassword(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, user_id):
        form = ChangePasswordForm()

        context = {
            'form': form
        }


        return render(request, 'users/userprofilepassword.html', context)
    


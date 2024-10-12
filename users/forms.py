# users/forms.py
from django import forms
from users.models import User, UserProfile
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.core.validators import RegexValidator
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm

class UserRegistrationForm(ModelForm):

    # สร้างรูปแบบการค้นหา
    phone_validator = RegexValidator(
        regex=r'^(0[0-9]{1})[0-9]{8}$',  # รูปแบบสำหรับหมายเลขมือถือไทย  ^: เริ่มต้น  0: ตัวแรกต้องเป็น 0 [0-9]{1}: หลังจาก 0 ต้องมี 0-9 เพียงหนึ่งหลัก [0-9]{8}: หมายถึงจะต้องมีตัวเลขอีก 8 หลักตามหลัง รวมกันแล้วจะต้องเป็นหมายเลขโทรศัพท์ทั้งหมด 10 หลัก $:จุดสิ้นสุด
        message="หมายเลขโทรศัพท์ต้องเป็นหมายเลขโทรศัพท์มือถือที่ถูกต้อง เช่น 0812345678."
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                          'placeholder': 'กรอกรหัสผ่าน'})
    )

    agree_terms = forms.BooleanField(
        required=True,
        label="ฉันยอมรับข้อตกลงของเว็บไซต์ Ticket Bever",
        error_messages={'required': 'กรุณายอมรับข้อตกลง'},
        widget=forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600 kanit-small'})
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
            'placeholder': 'กรอกรหัสผ่านยีนยัน'
        })
    )
    
    gender = forms.ChoiceField(
        choices=[
            (None, 'กรุณาเลือกเพศ'),
            ('M', 'ชาย'),
            ('F', 'หญิง'),
            ('O', 'อื่นๆ')
        ],
        widget=forms.Select(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 kanit-small'
        })  
    )

    telephone = forms.CharField(
        max_length=15,
        validators=[phone_validator],  
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
            'placeholder': '0812345678'  
        })
    )

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'border border-gray-300 rounded-md p-2 w-full kanit-small', 'placeholder': 'วันเกิด'})
    )

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password',
            'first_name',
            'last_name',
            'gender', 
            'telephone', 
            'date_of_birth'
        ] 

        widgets = {
            'username': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                               'placeholder': 'กรอกชื่อผู้ใช้งาน'}),
            'email': forms.EmailInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                             'placeholder': 'กรอกอีเมล'}),
            'first_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                                 'placeholder': 'กรอกชื่อจริงของคุณ'}),
            'last_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                                'placeholder': 'กรอกนามสกุลของคุณ'}),
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            # ดึงวันที่ ณ ปัจจุบัน มา ลบ ข้อมูลที่ได้จาก form date_of_birth แล้วมาทำเป็นปี โดยทำเป็นวันก่อนแล้วหาร 365
            age = (timezone.now().date() - date_of_birth).days // 365     # คำนวณอายุ
            if age < 13:
                raise ValidationError("คุณต้องมีอายุมากกว่า 13 ปีในการลงทะเบียนเข้าใช้ระบบนี้")
        return date_of_birth
    
    # ตรวจระดับ field
    def clean_password(self):
        password = self.cleaned_data.get("password")
        # ตรวจสอบความยาวของรหัสผ่าน
        if password and len(password) <= 9:
            raise ValidationError("รหัสผ่านต้องมีความยาวมากกว่า 9 ตัวอักษร")
        return password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get("confirm_password")
        password = self.cleaned_data.get("password")

        # ตรวจสอบว่าตรงกับรหัสยืนยันไหม
        if password and confirm_password and password != confirm_password:
            raise ValidationError("รหัสผ่านและยืนยันรหัสผ่านต้องตรงกัน")
        
        return confirm_password




class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='ชื่อผู้ใช้หรืออีเมล',
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small',  # เพิ่ม class สำหรับตกแต่ง
            'placeholder': 'กรุณากรอกชื่อผู้ใช้หรืออีเมล'
        })
    )
    password = forms.CharField(
        label='รหัสผ่าน',
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small',  # เพิ่ม class สำหรับตกแต่ง
            'placeholder': 'กรุณากรอกรหัสผ่าน'
        })
    )    


# Form vs ModelForm
# ModelForm เหมาะกับตรวจและบันทึกข้อมูล
# Form เหมาะกับข้อมูลไม่ตรงกับโมเดล

class ChangePasswordForm(forms.Form):

    email = forms.EmailField(label='อีเมล', widget=forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                             'placeholder': 'กรอกอีเมลของคุณ'}))

    def clean_email(self):
        # ดึงค่า email และ ตรวจสอบ + ทำความสะอาดข้อมูล
        email = self.cleaned_data.get('email')
        # ตรวจสอบว่ามีข้อมูลในตาราง User ไหม ใช้ .exists() ตรวจ
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("อีเมลนี้ไม่มีในระบบ")
        return email
    
        
class UserPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label='รหัสผ่านเดิม',
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small',
            'placeholder': 'กรุณากรอกรหัสผ่านเดิม'
        })
    )

    new_password1 = forms.CharField(
        label='รหัสผ่านใหม่',
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small',
            'placeholder': 'กรุณากรอกรหัสผ่านใหม่'
        })
    )

    new_password2 = forms.CharField(
        label='ยืนยันรหัสผ่านใหม่',
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small',
            'placeholder': 'กรุณายืนยันรหัสผ่านใหม่'
        })
    ) 

class UserSetPasswordForm(SetPasswordForm):

    new_password1 = forms.CharField(
        label='รหัสผ่านใหม่',
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small',
            'placeholder': 'กรุณากรอกรหัสผ่านใหม่'
        })
    )

    new_password2 = forms.CharField(
        label='ยืนยันรหัสผ่านใหม่',
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small',
            'placeholder': 'กรุณายืนยันรหัสผ่านใหม่'
        })
    ) 

class AttendeeForm(ModelForm):

     # สร้างรูปแบบการค้นหา
    phone_validator = RegexValidator(
        regex=r'^(0[0-9]{1})[0-9]{8}$',  # รูปแบบสำหรับหมายเลขมือถือไทย  ^: เริ่มต้น  0: ตัวแรกต้องเป็น 0 [0-9]{1}: หลังจาก 0 ต้องมี 0-9 เพียงหนึ่งหลัก [0-9]{8}: หมายถึงจะต้องมีตัวเลขอีก 8 หลักตามหลัง รวมกันแล้วจะต้องเป็นหมายเลขโทรศัพท์ทั้งหมด 10 หลัก $:จุดสิ้นสุด
        message="หมายเลขโทรศัพท์ต้องเป็นหมายเลขโทรศัพท์มือถือที่ถูกต้อง เช่น 0812345678."
    )

    telephone = forms.CharField(
        max_length=20,
        validators=[phone_validator],  
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
            'placeholder': '0812345678'  
        })
    )

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'border border-gray-300 rounded-md p-2 w-full kanit-small', 'placeholder': 'วันเกิด'})
    )


    class Meta:
        model = User
        fields = [ 
            'email', 
            'first_name',
            'last_name', 
            'telephone',
            'date_of_birth'
        ] 

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                             'placeholder': 'กรอกอีเมล'}),
            'first_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                                 'placeholder': 'กรอกชื่อจริงของคุณ'}),
            'last_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                                'placeholder': 'กรอกนามสกุลของคุณ'}),
        }
        
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            # ดึงวันที่ ณ ปัจจุบัน มา ลบ ข้อมูลที่ได้จาก form date_of_birth แล้วมาทำเป็นปี โดยทำเป็นวันก่อนแล้วหาร 365
            age = (timezone.now().date() - date_of_birth).days // 365     # คำนวณอายุ
            if age < 13:
                raise ValidationError("คุณต้องมีอายุมากกว่า 13 ปีในการลงทะเบียนเข้าใช้ระบบนี้")
        return date_of_birth


class UserProfileForm(ModelForm):

    profile_picture = forms.ImageField(
        required=False,  
        widget=forms.ClearableFileInput(attrs={
            'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
            'type': 'file',
            'id': 'file_input',
            'placeholder': 'เลือกรูปโปรไฟล์'
        })
    )
    
    # สร้างรูปแบบการค้นหา
    phone_validator = RegexValidator(
        regex=r'^(0[0-9]{1})[0-9]{8}$',  # รูปแบบสำหรับหมายเลขมือถือไทย  ^: เริ่มต้น  0: ตัวแรกต้องเป็น 0 [0-9]{1}: หลังจาก 0 ต้องมี 0-9 เพียงหนึ่งหลัก [0-9]{8}: หมายถึงจะต้องมีตัวเลขอีก 8 หลักตามหลัง รวมกันแล้วจะต้องเป็นหมายเลขโทรศัพท์ทั้งหมด 10 หลัก $:จุดสิ้นสุด
        message="หมายเลขโทรศัพท์ต้องเป็นหมายเลขโทรศัพท์มือถือที่ถูกต้อง เช่น 0812345678."
    )
    
    gender = forms.ChoiceField(
        choices=[
            (None, 'กรุณาเลือกเพศ'),
            ('M', 'ชาย'),
            ('F', 'หญิง'),
            ('O', 'อื่นๆ')
        ],
        widget=forms.Select(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 kanit-small'
        })  
    )

    telephone = forms.CharField(
        max_length=15,
        validators=[phone_validator],  
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
            'placeholder': '0812345678'  
        })
    )

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'border border-gray-300 rounded-md p-2 w-full kanit-small', 'placeholder': 'วันเกิด'})
    )

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'first_name',
            'last_name',
            'gender', 
            'telephone', 
            'date_of_birth',
            'profile_picture',
        ] 

        widgets = {
            'username': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                               'placeholder': 'กรอกชื่อผู้ใช้งาน'}),
            'email': forms.EmailInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                             'placeholder': 'กรอกอีเมล'}),
            'first_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                                 'placeholder': 'กรอกชื่อจริงของคุณ'}),
            'last_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                                'placeholder': 'กรอกนามสกุลของคุณ'}),
        }
    

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            # ดึงวันที่ ณ ปัจจุบัน มา ลบ ข้อมูลที่ได้จาก form date_of_birth แล้วมาทำเป็นปี โดยทำเป็นวันก่อนแล้วหาร 365
            age = (timezone.now().date() - date_of_birth).days // 365     # คำนวณอายุ
            if age < 13:
                raise ValidationError("คุณต้องมีอายุมากกว่า 13 ปีในการลงทะเบียนเข้าใช้ระบบนี้")
        return date_of_birth


    




    
    

from django import forms
from users.models import User
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

class UserRegistrationForm(ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
                                          'placeholder': 'กรอกรหัสผ่าน'})
    )

    agree_terms = forms.BooleanField(
        required=True,
        label="ฉันยอมรับข้อตกลงของเว็บไซต์ Ticket Bever",
        error_messages={'required': 'กรุณายอมรับข้อตกลง'},
        widget=forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'})
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
            'placeholder': 'กรอกรหัสผ่านยีนยัน'
        })
    )
    
    gender = forms.ChoiceField(
        choices=[
            (None, 'กรุราเลือกเพศ'),
            ('M', 'ชาย'),
            ('F', 'หญิง'),
            ('O', 'อื่นๆ')
        ],
        widget=forms.Select(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'
        })  
    )

    telephone = forms.CharField(max_length=15, 
                                widget=forms.TextInput(attrs={
                                    'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
                                    'placeholder': '081 234 5678'
                                }))

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'border border-gray-300 rounded-md p-2 w-full', 'placeholder': 'วันเกิด'})
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
            'username': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
                                               'placeholder': 'กรอกชื่อผู้ใช้งาน'}),
            'email': forms.EmailInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
                                             'placeholder': 'กรอกอีเมล'}),
            'first_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
                                                 'placeholder': 'กรอกชื่อจริงของคุณ'}),
            'last_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500', 
                                                'placeholder': 'กรอกนามสกุลของคุณ'}),
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            # ดึงวันที่ ณ ปัจจุบัน มา ลบ ข้อมูลที่ได้จาก form date_of_birth แล้วมาทำเป็นปี โดยทำเป็นวันก่อนแล้วหาร 365
            age = (timezone.now().date() - date_of_birth).days // 365     # คำนวณอายุ
            if age < 10:
                raise ValidationError("คุณต้องมีอายุมากกว่า 10 ปีในการลงทะเบียนเข้าใช้ระบบนี้")
        return date_of_birth
    
    # ตรวจระดับ form
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # ตรวจสอบความยาวของรหัสผ่าน
        if password:
            if len(password) <= 9:
                raise ValidationError("รหัสผ่านต้องมีความยาวมากกว่า 9 ตัวอักษร")
            
        # ตรวจสอบว่าตรงกับรหัสยืนยันไหม
        if password and confirm_password and password != confirm_password:
            raise ValidationError("รหัสผ่านและยืนยันรหัสผ่านต้องตรงกัน")

        return cleaned_data
        
    
        
    



    
    

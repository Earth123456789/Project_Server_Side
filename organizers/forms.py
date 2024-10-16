from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm
from organizers.models import *

class CompanyRegistrationForm(ModelForm):

    COMPANY_TYPE_CHOICES = [
        ('บริษัท', 'บริษัท'),
        ('บุคคล', 'บุคคล')
    ]

    phone_validator = RegexValidator(
        regex=r'^(0[0-9]{1})[0-9]{8}$',
        message="หมายเลขโทรศัพท์ต้องเป็นหมายเลขโทรศัพท์มือถือที่ถูกต้อง เช่น 0812345678."
    )

    agree_terms = forms.BooleanField(
        required=True,
        label="ฉันยอมรับข้อตกลงของเว็บไซต์ Ticket Bever",
        error_messages={'required': 'กรุณายอมรับข้อตกลง'},
        widget=forms.CheckboxInput(
            attrs={
                'class': (
                    'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded '
                    'focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 '
                    'focus:ring-2 dark:bg-gray-700 dark:border-gray-600 kanit-small'
                )
            }
        )
    )

    telephone = forms.CharField(
        max_length=15,
        validators=[phone_validator],
        widget=forms.TextInput(
            attrs={
                'class': (
                    'bg-gray-50 border border-gray-300 text-gray-900 text-sm '
                    'rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '
                    'dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white '
                    'dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small'
                ),
                'placeholder': '0812345678'
            }
        )
    )

    type = forms.ChoiceField(
        choices=COMPANY_TYPE_CHOICES,  
        widget=forms.Select(
            attrs={
                'class': (
                    'bg-gray-50 border border-gray-300 text-gray-900 text-sm '
                    'rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '
                    'dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white '
                    'dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small'
                )
            }
        )
    )

    class Meta:
        model = Company
        fields = ['name', 'email', 'telephone', 'contact', 'type', 'agree_terms']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': (
                        'bg-gray-50 border border-gray-300 text-gray-900 text-sm '
                        'rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '
                        'dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white '
                        'dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small'
                    ),
                    'placeholder': 'ชื่อบริษัท'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': (
                        'bg-gray-50 border border-gray-300 text-gray-900 text-sm '
                        'rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '
                        'dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white '
                        'dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small'
                    ),
                    'placeholder': 'กรอกอีเมล'
                }
            ),
            'contact': forms.URLInput(
                attrs={
                    'class': (
                        'bg-gray-50 border border-gray-300 text-gray-900 text-sm '
                        'rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '
                        'dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white '
                        'dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small'
                    ),
                    'placeholder': 'เว็บไซต์หรือช่องทางการติดต่อ'
                }
            ),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "description", "location", "start_date", "start_time", "end_date", "end_time", "image", "max_participants", "category", "ticket_price"]

class CompanyDetailForm(ModelForm):
    phone_validator = RegexValidator(
        regex=r'^(0[0-9]{1})[0-9]{8}$',
        message="หมายเลขโทรศัพท์ต้องเป็นหมายเลขโทรศัพท์มือถือที่ถูกต้อง เช่น 0812345678."
    )

    telephone = forms.CharField(
        max_length=15,
        validators=[phone_validator],  
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
            'placeholder': '0812345678'  
        })
    )

    class Meta:
        model = Company
        fields = ['name', 'email', 'telephone', 'contact'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                                'placeholder': 'กรอกชื่อบริษัท'}),
            'email': forms.EmailInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                                'placeholder': 'กรอกอีเมล'}),
            'telephone': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                                'placeholder': 'กรอกเบอร์โทรศัพท์องค์กร'}),
            'contact': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 kanit-small', 
                                                'placeholder': 'กรอกช่องทางติดต่อขององค์กร'}),
        }

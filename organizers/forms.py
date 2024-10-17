from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
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

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),  
        widget=forms.Select(attrs={
            'class': 'kanit-small border rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-500'
        }),
        empty_label="เลือกหมวดหมู่" 
    )

    class Meta:
        model = Event
        fields = [
            "name", "description", "location", "start_date", "start_time",
            "end_date", "end_time", "image", "max_participants", "category", "ticket_price"
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'kanit-small border rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-500'}),
            'description': forms.Textarea(attrs={'class': 'kanit-small border rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-500'}),
            'location': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 kanit-small', 'id': 'location-autocomplete'}),
            'start_date': forms.DateInput(attrs={'class': 'kanit-small border rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-500', 'type': 'date'  }),
            'start_time': forms.TimeInput(attrs={'class': 'kanit-small border rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-500', 'type': 'time' }),
            'end_date': forms.DateInput(attrs={'class': 'kanit-small border rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-500', 'type': 'date'  }),
            'end_time': forms.TimeInput(attrs={'class': 'kanit-small border rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-500', 'type': 'time' }),
            'image': forms.FileInput(attrs={'class': 'kanit-small border rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-500'}),
            'max_participants': forms.NumberInput(attrs={'class': 'kanit-small border rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-500'}),
            'ticket_price': forms.NumberInput(attrs={'class': 'kanit-small border rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-500'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        start_time = cleaned_data.get("start_time")
        end_date = cleaned_data.get("end_date")
        end_time = cleaned_data.get("end_time")

        # รวม filed date time เพื่อเทียบกับเวลาปัจจุบันที่เกิดขึ้น
        if start_date and start_time:
            start_datetime = timezone.make_aware(datetime.combine(start_date, start_time), timezone.get_current_timezone())
            if start_datetime < timezone.now():
                raise ValidationError("วันและเวลาจัดกิจกรรมต้องไม่อยู่ในอดีต")

        if end_date and end_time:
            end_datetime = timezone.make_aware(datetime.combine(end_date, end_time), timezone.get_current_timezone())
            if end_datetime < timezone.now():
                raise ValidationError("วันและเวลาสิ้นสุดกิจกรรมต้องไม่อยู่ในอดีต")
            
            # แบบ week 8-9
            if start_datetime and end_datetime and end_datetime < start_datetime:
                raise ValidationError("วันสิ้นสุดกิจกรรมต้องไม่มาก่อนวันจัดกิจกรรม")

        return cleaned_data

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


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = [
            "name", "description"
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'kanit-small border rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-500'}),
            'description': forms.Textarea(attrs={'class': 'kanit-small border rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-500'}),
        }
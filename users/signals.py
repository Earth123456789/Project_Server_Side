# เก็บรูปลง Userprofile

from allauth.account.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount
from django.dispatch import receiver
from .models import UserProfile


# เมื่อเหตุการณ์ update_profile ถูกส่งออกมา สัญญาณนี้ถูกส่งเมื่อผู้ใช้ทำการเข้าสู่ระบบสำเร็จ ใช้เพื่อ ทำการบันทึกข้อมูลในฐานข้อมูล
@receiver(user_logged_in)
# **kwargs : สามารถรับค่าได้ตามที่ต้องการ
def update_profile(request, user, **kwargs):
    try:
        # ดึงข้อมูลจากตาราง SocialAccount 
        social_account = SocialAccount.objects.get(user=user)
        extra_data = social_account.extra_data
        print(f"Extra data from Google: {extra_data}")

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.profile_picture = extra_data.get('picture', '')
        profile.save()

    except SocialAccount.DoesNotExist:
        print("หาข้อมูลผู้ใช้งานที่ลงทะเบียนด้วย google ไม่พบ")
    except UserProfile.DoesNotExist:
        print(f"ไม่มีข้อมูลโปรไฟล์ของ : {user}.")


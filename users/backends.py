# สร้าง custom authentication backend โดยจะเรียกใน setting.py
# users/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class UsernameOrEmailBackend(ModelBackend):

    # function ของ django ที่ใช้สำหรับตรวจสอบและยืนยันข้อมูลการล็อกอินของผู้ใช้
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # ตรวจสอบว่าข้อมูลที่ส่งมาคือ email หรือ username
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)

        # ไม่มีการค้นพบผู้ใช้ในฐานข้อมูล
        except User.DoesNotExist:
            return None

        # ตรวจสอบรหัสผ่าน
        if user.check_password(password):
            return user
        return None
    
    # ดึงข้อมูลผู้ใช้งาน
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

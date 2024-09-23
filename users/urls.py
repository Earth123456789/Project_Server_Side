from django.urls import path
from users.views import RegisterView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
] 

# ตั้งค่าเพื่อให้ใช้ รูปที่มาจาก media (imagefiled) ได้
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
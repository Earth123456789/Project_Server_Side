# users/url.py
from django.urls import path
from users.views import RegisterView, LoginView, LogoutView, ChangePasswordView, PasswordResetConfirmView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('password_reset/', ChangePasswordView.as_view(), name='password_reset'),
    path('password_reset_confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
] 

# ตั้งค่าเพื่อให้ใช้ รูปที่มาจาก media (imagefiled) ได้
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# users/url.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from users.views import RegisterView, LoginView, LogoutView, ChangePasswordView, PasswordResetConfirmView, ReceiveTicketView, AttendeeView, PaymentView , ValidateView ,SuccessView, UserProfileView, UserChangePassword, PasswordChangeConfirmView, TicketView, TicketDeatilView, TicketPastView, TicketSent, TransactionSuccessView, TransactionVerificationView, TransactionFailedView, TransactionDetailView


urlpatterns = [
    # Auth Path
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password_reset/", ChangePasswordView.as_view(), name="password_reset"),
    path("password_reset_confirm/<str:uidb64>/<str:token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),


    # User Ticket Path
    path("event/receive/<int:event_id>/", ReceiveTicketView.as_view(), name="receive_ticket" ),
    path("event/attendent/<int:event_id>/<str:uidb64>/<str:token>/", AttendeeView.as_view(), name="attendent"),
    path("event/payment/<int:event_id>/<str:uidb64>/<str:token>/", PaymentView.as_view(), name='payment'),
    path("event/validate/<int:event_id>/<str:uidb64>/<str:token>/", ValidateView.as_view(), name='validate'),
    path("event/success/<int:event_id>/<str:uidb64>/<str:token>/", SuccessView.as_view(), name="success"),


    # User Profile Path
    path("<int:user_id>/", UserProfileView.as_view(), name="userprofile" ),
    path("ticket/<int:user_id>/", TicketView.as_view(), name="ticket" ),
    path("ticket/<int:user_id>/send/<int:ticket_id>/", TicketSent.as_view(), name="send_ticket"),
    path("ticket/<int:user_id>/detail/<int:ticket_id>/", TicketDeatilView.as_view(), name="ticketdetail" ),
    path("ticket/past/<int:user_id>/", TicketPastView.as_view(), name="ticketpast" ),
    path("change_password/<int:user_id>/", UserChangePassword.as_view(), name="changepassword" ),
    path("password_change_confirm/<str:uidb64>/<str:token>/", PasswordChangeConfirmView.as_view(), name="password_change_confirm"),
    path("transaction/<int:user_id>/success/", TransactionSuccessView.as_view(), name="transaction-success"),
    path("transaction/<int:user_id>/verification/", TransactionVerificationView.as_view(), name="transaction-verification"),
    path("transaction/<int:user_id>/failed/", TransactionFailedView.as_view(), name="transaction-failed"),
     path("transaction/<int:user_id>/detail/<int:payment_id>/", TransactionDetailView.as_view(), name="transaction-deatil"),

    # Test - When Event Success อยู่ ผู้จัด Event
    path("success/<int:user_id>/", TransactionSuccessView.as_view(), name="success-mail" ),
] 

# ตั้งค่าเพื่อให้ใช้ รูปที่มาจาก media (imagefiled) ได้
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
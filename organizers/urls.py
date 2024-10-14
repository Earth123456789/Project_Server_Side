# organizers/url.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from organizers.views import OrganizerRegisterView, DashBoardView, TransactionView, CancelTransactionView


urlpatterns = [
    # Auth Path
    path("register/", OrganizerRegisterView.as_view(), name="organizer-register"),

    # Organizers Path
    path("dashboard/<int:company_id>/", DashBoardView.as_view(), name="dashboard"),
    path("transaction/<int:company_id>/", TransactionView.as_view(), name="transaction"),
    path("transaction/cancel/<int:company_id>/", CancelTransactionView.as_view(), name='cancel_transaction'),
] 

# ตั้งค่าเพื่อให้ใช้ รูปที่มาจาก media (imagefiled) ได้
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
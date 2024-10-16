from django.urls import path
from general.views import HomepageView, EventView, ChatView, ChatBotView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Event
    path("", HomepageView.as_view(), name="homepage"),
    path("event/<int:event_id>/", EventView.as_view(), name="event"),
    path("event/<int:event_id>/followers/<int:user_id>/", EventView.as_view(), name="follower"),
    path("chat/<int:user_id>", ChatView.as_view(), name='chatbot'),
    path('api/chat/', ChatBotView.as_view(), name='chatbot_api'),
] 

# ตั้งค่าเพื่อให้ใช้ รูปที่มาจาก media (imagefiled) ได้
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
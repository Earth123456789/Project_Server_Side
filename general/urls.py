from django.urls import path
from general.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", HomepageView.as_view(), name="employee"),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
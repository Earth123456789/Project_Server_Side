from django.contrib import admin

from users.models import *

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(EventParticipant)
admin.site.register(Ticket)
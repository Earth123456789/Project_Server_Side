from django.contrib.auth.models import Group
from django.dispatch import receiver

from allauth.account.signals import user_signed_up, user_logged_in

# signals.py ใช้เพื่อจัดการ app ของ django ช่วยให้ app แยกส่วนการทำงานกัน
# https://docs.djangoproject.com/en/5.1/topics/signals/#:~:text=Django%E2%80%99s%20built-in%20signals%20let%20user%20code%20get%20notified%20of
@receiver(user_logged_in)
def add_user_to_group_on_login(sender, request, user, **kwargs):
    user_group = Group.objects.get(name='Users')
    user.groups.add(user_group)

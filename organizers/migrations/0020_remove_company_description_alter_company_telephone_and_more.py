# Generated by Django 5.1.2 on 2024-10-12 05:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0019_company_type_company_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='description',
        ),
        migrations.AlterField(
            model_name='company',
            name='telephone',
            field=models.CharField(default='0000000000', max_length=15),
        ),
        migrations.AlterField(
            model_name='company',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
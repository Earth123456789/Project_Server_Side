# Generated by Django 5.1.2 on 2024-10-14 04:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0023_remove_payment_event_payment_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='organizers.event'),
            preserve_default=False,
        ),
    ]
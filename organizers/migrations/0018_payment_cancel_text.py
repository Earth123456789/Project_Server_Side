# Generated by Django 5.1.1 on 2024-10-10 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0017_alter_event_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='cancel_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]

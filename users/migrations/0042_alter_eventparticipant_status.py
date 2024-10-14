# Generated by Django 5.1.2 on 2024-10-14 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0041_alter_eventparticipant_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventparticipant',
            name='status',
            field=models.CharField(choices=[('Register', 'Register'), ('Attended', 'Attended'), ('Cancelled', 'Cancelled'), ('No Show', 'No Show')], default='No Show', max_length=30),
        ),
    ]

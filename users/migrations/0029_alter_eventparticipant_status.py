# Generated by Django 5.1.1 on 2024-10-09 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_alter_eventparticipant_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventparticipant',
            name='status',
            field=models.CharField(choices=[('Register', 'Register'), ('Attended', 'Attended'), ('Cancelled', 'Cancelled'), ('No Show', 'No Show')], default='No Show', max_length=30),
        ),
    ]

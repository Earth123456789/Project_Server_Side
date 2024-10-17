# Generated by Django 5.1.1 on 2024-10-05 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_alter_eventparticipant_status_alter_ticket_qr_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventparticipant',
            name='status',
            field=models.CharField(choices=[('Register', 'Register'), ('Attended', 'Attended'), ('Cancelled', 'Cancelled'), ('No Show', 'No Show')], default='No Show', max_length=30),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('Valid', 'Valid'), ('Used', 'Used'), ('Expired', 'Expired')], default='Valid', max_length=15),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-05 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0005_event_ticket_price_payment_ticket_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('Show', 'Show'), ('Close', 'Close'), ('Past', 'Past')], default='Show', max_length=10),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-01 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0004_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='ticket_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.AddField(
            model_name='payment',
            name='ticket_quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]

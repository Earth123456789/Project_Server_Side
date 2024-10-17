# Generated by Django 5.1.1 on 2024-10-05 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0007_alter_event_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('Show', 'Show'), ('Close', 'Close'), ('Past', 'Past')], default='Show', max_length=10),
        ),
    ]

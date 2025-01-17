# Generated by Django 5.1.1 on 2024-09-26 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_userprofile_image_userprofile_profile_picture_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='eventparticipant',
            name='status',
            field=models.CharField(choices=[('Register', 'Register'), ('Attended', 'Attended'), ('Cancelled', 'Cancelled'), ('No Show', 'No Show')], default='No Show', max_length=15),
        ),
    ]

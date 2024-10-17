# Generated by Django 5.1.2 on 2024-10-12 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0020_remove_company_description_alter_company_telephone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='type',
            field=models.CharField(choices=[('บริษัท', 'บริษัท'), ('บุคคล', 'บุคคล')], default='บุคคล', max_length=10),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-25 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_cuser_is_active_remove_cuser_is_admin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuser',
            name='phone_number',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='personalcontact',
            name='phone_number',
            field=models.CharField(max_length=10),
        ),
    ]

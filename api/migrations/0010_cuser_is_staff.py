# Generated by Django 4.2.7 on 2023-11-25 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_cuser_is_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]

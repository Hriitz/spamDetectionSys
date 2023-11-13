# Generated by Django 4.2.7 on 2023-11-13 03:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_spamnumber_email_spamnumber_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuser',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='cuser',
            name='is_admin',
        ),
        migrations.AlterField(
            model_name='spamnumber',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
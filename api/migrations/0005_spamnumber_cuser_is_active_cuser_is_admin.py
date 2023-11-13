# Generated by Django 4.2.7 on 2023-11-12 13:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_personalcontact_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpamNumber',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='cuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cuser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]

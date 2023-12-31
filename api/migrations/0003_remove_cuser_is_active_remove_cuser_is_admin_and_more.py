# Generated by Django 4.2.7 on 2023-11-12 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_cuser_delete_customuser'),
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
            model_name='cuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.CreateModel(
            name='PersonalContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personal_contacts', to='api.cuser')),
            ],
        ),
    ]

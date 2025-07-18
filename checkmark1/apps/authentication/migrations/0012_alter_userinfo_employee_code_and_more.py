# Generated by Django 5.0.4 on 2024-05-15 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_alter_userinfo_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='employee_code',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='national_code',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]

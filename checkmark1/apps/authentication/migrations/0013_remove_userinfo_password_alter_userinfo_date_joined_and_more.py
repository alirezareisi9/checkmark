# Generated by Django 5.0.4 on 2024-05-15 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_alter_userinfo_employee_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='password',
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='last_login',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

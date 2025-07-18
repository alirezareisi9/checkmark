# Generated by Django 5.0.4 on 2024-05-08 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_userinfo_leave_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='role',
            field=models.CharField(choices=[('EMPLOYEE', 'Employee'), ('REPORTER', 'Reporter'), ('MANAGER', 'Manager')], default='EMPLOYEE', max_length=255),
        ),
    ]

# Generated by Django 5.0.4 on 2024-05-18 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0011_log_approved_by_log_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]

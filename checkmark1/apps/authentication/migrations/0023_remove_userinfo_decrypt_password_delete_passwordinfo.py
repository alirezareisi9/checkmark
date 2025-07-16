

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0022_remove_passwordinfo_user_userinfo_decrypt_password_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='decrypt_password',
        ),
        migrations.DeleteModel(
            name='PasswordInfo',
        ),
    ]

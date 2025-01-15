# Generated by Django 4.2.5 on 2025-01-14 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='isProf',
            new_name='is_Professor',
        ),
        migrations.AlterField(
            model_name='appointment',
            name='professor',
            field=models.ForeignKey(limit_choices_to={'is_Professor': True}, on_delete=django.db.models.deletion.CASCADE, related_name='professor_appointments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='availability',
            name='prof',
            field=models.ForeignKey(limit_choices_to={'is_Professor': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 5.1.1 on 2024-11-23 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_remove_user_reported_user_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lang',
            field=models.TextField(default=''),
        ),
    ]
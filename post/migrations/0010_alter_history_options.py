# Generated by Django 5.1.1 on 2024-09-22 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_alter_history_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='history',
            options={'ordering': ['-created_at']},
        ),
    ]
# Generated by Django 5.1.1 on 2024-10-22 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0017_alter_history_liked_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='liked_at',
        ),
        migrations.AlterField(
            model_name='history',
            name='favorited_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
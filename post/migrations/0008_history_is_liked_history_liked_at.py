# Generated by Django 5.1.1 on 2024-09-22 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_remove_post_favorited_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='is_liked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='history',
            name='liked_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-20 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0015_evaluation_prompt'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='referenceActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-20 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_alter_evaluation_death_harm_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='contentChecked',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='post',
            name='referenceChecked',
            field=models.BooleanField(default=True),
        ),
    ]
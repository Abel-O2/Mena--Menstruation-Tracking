# Generated by Django 5.1.3 on 2024-11-27 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MenaApp', '0008_cyclephase_mood'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendar',
            name='end_time',
        ),
        migrations.AlterField(
            model_name='calendar',
            name='start_time',
            field=models.DateField(blank=True, null=True),
        ),
    ]

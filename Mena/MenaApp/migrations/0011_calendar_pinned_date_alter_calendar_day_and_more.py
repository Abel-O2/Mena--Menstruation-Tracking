# Generated by Django 5.1.3 on 2024-11-27 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MenaApp', '0010_calendar_day_calendar_end_time_calendar_month_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='pinned_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='day',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='month',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='year',
            field=models.IntegerField(),
        ),
    ]
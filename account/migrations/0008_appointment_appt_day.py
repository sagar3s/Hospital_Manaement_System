# Generated by Django 3.0.5 on 2021-06-03 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20210603_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='appt_day',
            field=models.DateField(null=True),
        ),
    ]

# Generated by Django 3.1.7 on 2021-04-05 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 2.2.1 on 2019-05-17 07:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pkchanger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileNameModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=50)),
                ('upload_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]

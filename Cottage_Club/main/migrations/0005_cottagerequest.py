# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20150105_0914'),
    ]

    operations = [
        migrations.CreateModel(
            name='CottageRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='Email', blank=True)),
                ('arrival_date', models.DateField(verbose_name='Arrival Date', blank=True)),
                ('departure_date', models.DateField(verbose_name='Departure Date', blank=True)),
                ('additional_info', models.TextField(verbose_name='Additional Info', blank=True)),
                ('phone', models.CharField(max_length=20, blank=True)),
            ],
            options={
                'verbose_name': 'Request',
                'verbose_name_plural': 'Requests',
            },
            bases=(models.Model,),
        ),
    ]

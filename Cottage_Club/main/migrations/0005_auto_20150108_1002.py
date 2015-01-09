# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20150105_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dateprices',
            name='end_date',
            field=models.DateField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dateprices',
            name='start_date',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]

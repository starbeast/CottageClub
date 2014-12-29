# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20141226_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cottage',
            name='category',
            field=models.ForeignKey(blank=True, to='main.Category', null=True),
            preserve_default=True,
        ),
    ]

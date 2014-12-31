# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20141231_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='is_separator',
            field=models.BooleanField(default=False, verbose_name='Will be a separator'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attribute',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Order in the list'),
            preserve_default=True,
        ),
    ]

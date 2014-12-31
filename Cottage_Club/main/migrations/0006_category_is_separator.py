# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20141231_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_separator',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150105_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cottage',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=1, max_length=250, blank=True),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150105_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cottage',
            name='slug',
            field=autoslug.fields.AutoSlugField(null=True, blank=True),
            preserve_default=True,
        ),
    ]

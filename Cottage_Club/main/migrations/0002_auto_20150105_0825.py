# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cottage',
            name='slug',
            field=autoslug.fields.AutoSlugField(null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cottage',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Object title'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_category_is_separator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='is_separator',
            field=models.BooleanField(default=False, verbose_name='Is separator'),
            preserve_default=True,
        ),
    ]

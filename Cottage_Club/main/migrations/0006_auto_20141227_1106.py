# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Cottage_Club.main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20141227_0801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='user',
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=Cottage_Club.main.models._upload_path_wrapper, verbose_name='Image'),
            preserve_default=True,
        ),
    ]

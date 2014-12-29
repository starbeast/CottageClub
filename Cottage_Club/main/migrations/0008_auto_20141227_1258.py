# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import storages.backends.overwrite
import Cottage_Club.main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20141227_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='caption',
            field=models.TextField(null=True, verbose_name='Caption', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='image',
            field=models.ImageField(default=b'images/generic_profile_photo.jpg', upload_to=Cottage_Club.main.models._upload_path_wrapper, storage=storages.backends.overwrite.OverwriteStorage(), verbose_name='Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='is_main',
            field=models.BooleanField(default=False, verbose_name='Main image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Order'),
            preserve_default=True,
        ),
    ]

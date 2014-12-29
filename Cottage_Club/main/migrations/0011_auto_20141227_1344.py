# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20141227_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(default=b'images/default_product.jpg', upload_to=b'cottage_images', storage=django.core.files.storage.FileSystemStorage(), verbose_name='Image'),
            preserve_default=True,
        ),
    ]

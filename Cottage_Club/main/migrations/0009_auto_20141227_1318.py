# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import storages.backends.overwrite


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20141227_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(default=b'/home/yulia/PycharmProjects/CottageClub/Cottage_Club/../media/images/generic_profile_photo.jpg', upload_to=b'/home/yulia/PycharmProjects/CottageClub/Cottage_Club/../media//cottage_images/', storage=storages.backends.overwrite.OverwriteStorage(), verbose_name='Image'),
            preserve_default=True,
        ),
    ]

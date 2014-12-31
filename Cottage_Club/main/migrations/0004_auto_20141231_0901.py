# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20141230_0904'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatePrices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(auto_now_add=True)),
                ('price', models.IntegerField(default=0)),
                ('cottage', models.ForeignKey(related_name='prices', verbose_name='Pricing', blank=True, to='main.Cottage', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cottage',
            name='detailed_description',
            field=tinymce.models.HTMLField(null=True, verbose_name='Detailed description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cottage',
            name='minimal_price',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(default=b'images/default_product.png', upload_to=b'cottage_images', storage=django.core.files.storage.FileSystemStorage(), verbose_name='Image'),
            preserve_default=True,
        ),
    ]

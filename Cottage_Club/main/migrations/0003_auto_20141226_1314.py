# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_cottage_sib_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['-order']},
        ),
        migrations.RenameField(
            model_name='image',
            old_name='entity_type',
            new_name='content_type',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='entity_id',
            new_name='object_id',
        ),
        migrations.RemoveField(
            model_name='image',
            name='url',
        ),
        migrations.AddField(
            model_name='image',
            name='caption',
            field=models.TextField(null=True, verbose_name='Caption', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='image',
            field=models.ImageField(default=1, upload_to='cottages', verbose_name='Image'),
            preserve_default=False,
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
        migrations.AddField(
            model_name='image',
            name='user',
            field=models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cottage',
            name='parent',
            field=models.ForeignKey(related_name='children', verbose_name='Parent object', blank=True, to='main.Cottage', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cottage',
            name='structure',
            field=models.CharField(default=b'parent', max_length=10, verbose_name='Object structure', choices=[(b'parent', 'Parent object'), (b'child', 'Inner object')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cottage',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Object title', blank=True),
            preserve_default=True,
        ),
    ]

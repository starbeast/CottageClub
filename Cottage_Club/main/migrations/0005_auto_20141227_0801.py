# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20141226_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='choice',
            field=models.ForeignKey(blank=True, to='main.Choice', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='attribute',
            name='schema',
            field=models.ForeignKey(related_name='attrs', to='main.Schema'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='choice',
            name='schema',
            field=models.ForeignKey(related_name='choices', to='main.Schema'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cottage',
            name='category',
            field=models.ForeignKey(blank=True, to='main.Category', help_text='leave blank if this is not a parent object', null=True),
            preserve_default=True,
        ),
    ]

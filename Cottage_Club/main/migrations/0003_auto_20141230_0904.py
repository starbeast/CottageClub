# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20141229_1507'),
    ]

    operations = [
        migrations.CreateModel(
            name='MpttTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='main.MpttTest', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchemaForMpttTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('will_be_a_filter', models.BooleanField(default=False)),
                ('name_on_forms', models.CharField(max_length=100, blank=True)),
                ('mptttest', models.ForeignKey(to='main.MpttTest')),
                ('schema', models.ForeignKey(to='main.Schema')),
            ],
            options={
                'verbose_name': 'Attribute of MPTT',
                'verbose_name_plural': 'Attributes of MPTT',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='schemaformptttest',
            unique_together=set([('schema', 'mptttest')]),
        ),
        migrations.AddField(
            model_name='mptttest',
            name='schemas',
            field=models.ManyToManyField(related_name='mptts', through='main.SchemaForMpttTest', to='main.Schema'),
            preserve_default=True,
        ),
    ]

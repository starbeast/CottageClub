# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import mptt.fields
import django.core.files.storage
import tinymce.models
import Cottage_Club.main.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity_id', models.IntegerField()),
                ('value_text', models.TextField(null=True, blank=True)),
                ('value_float', models.FloatField(null=True, blank=True)),
                ('value_date', models.DateField(null=True, blank=True)),
                ('value_bool', models.NullBooleanField()),
                ('value_range_min', models.FloatField(null=True, blank=True)),
                ('value_range_max', models.FloatField(null=True, blank=True)),
                ('description', models.CharField(max_length=200, blank=True)),
                ('is_separator', models.BooleanField(default=False, verbose_name='Will be a separator')),
                ('order', models.IntegerField(default=0, verbose_name='Order in the list')),
            ],
            options={
                'verbose_name': 'Attribute value',
                'verbose_name_plural': 'Attribute values',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lft', models.PositiveIntegerField(db_index=True)),
                ('rgt', models.PositiveIntegerField(db_index=True)),
                ('tree_id', models.PositiveIntegerField(db_index=True)),
                ('depth', models.PositiveIntegerField(db_index=True)),
                ('name', models.CharField(max_length=30)),
                ('is_separator', models.BooleanField(default=False, verbose_name='Is separator')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('title',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cottage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('structure', models.CharField(default=b'parent', max_length=10, verbose_name='Object structure', choices=[(b'parent', 'Parent object'), (b'child', 'Inner object')])),
                ('sib_order', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(max_length=255, verbose_name='Object title', blank=True)),
                ('minimal_price', models.IntegerField(default=0)),
                ('detailed_description', tinymce.models.HTMLField(null=True, verbose_name='Detailed description', blank=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('is_recommended', models.BooleanField(default=False)),
                ('is_banner', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('category', models.ForeignKey(blank=True, to='main.Category', help_text='leave blank if this is not a parent object', null=True)),
                ('parent', models.ForeignKey(related_name='children', verbose_name='Parent object', blank=True, to='main.Cottage', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
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
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('caption', models.TextField(null=True, verbose_name='Caption', blank=True)),
                ('is_main', models.BooleanField(default=False, verbose_name='Main image')),
                ('order', models.IntegerField(default=0, verbose_name='Order')),
                ('image', models.ImageField(default=b'images/default_product.png', upload_to=b'cottage_images', storage=django.core.files.storage.FileSystemStorage(), verbose_name='Image')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model, Cottage_Club.main.models.ImageContainingModel),
        ),
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
            name='Schema',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='user-friendly attribute name', max_length=250, verbose_name='title')),
                ('name', autoslug.fields.AutoSlugField(max_length=250, verbose_name='name', blank=True)),
                ('help_text', models.CharField(help_text='short description for administrator', max_length=250, verbose_name='help text', blank=True)),
                ('datatype', models.CharField(max_length=5, verbose_name='data type', choices=[(b'text', 'text'), (b'float', 'number'), (b'date', 'date'), (b'bool', 'boolean'), (b'one', 'choice'), (b'many', 'multiple choices'), (b'range', 'numeric range')])),
                ('required', models.BooleanField(default=False, verbose_name='required')),
                ('searched', models.BooleanField(default=False, verbose_name='include in search')),
                ('filtered', models.BooleanField(default=False, verbose_name='include in filters')),
                ('sortable', models.BooleanField(default=False, verbose_name='allow sorting')),
            ],
            options={
                'verbose_name': 'Attribute',
                'verbose_name_plural': 'Attributes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchemaForCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('will_be_a_filter', models.BooleanField(default=False)),
                ('name_on_forms', models.CharField(max_length=100, blank=True)),
                ('category', models.ForeignKey(to='main.Category')),
                ('schema', models.ForeignKey(to='main.Schema')),
            ],
            options={
                'verbose_name': 'Attribute of Category',
                'verbose_name_plural': 'Attributes of Category',
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
        migrations.AlterUniqueTogether(
            name='schemaforcategory',
            unique_together=set([('schema', 'category')]),
        ),
        migrations.AddField(
            model_name='mptttest',
            name='schemas',
            field=models.ManyToManyField(related_name='mptts', through='main.SchemaForMpttTest', to='main.Schema'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='choice',
            name='schema',
            field=models.ForeignKey(related_name='choices', to='main.Schema'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='schemas',
            field=models.ManyToManyField(related_name='categories', through='main.SchemaForCategory', to='main.Schema'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attribute',
            name='choice',
            field=models.ForeignKey(blank=True, to='main.Choice', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attribute',
            name='entity_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attribute',
            name='schema',
            field=models.ForeignKey(related_name='attrs', to='main.Schema'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


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
            ],
            options={
                'ordering': ['entity_type', 'entity_id', 'schema'],
                'abstract': False,
                'verbose_name': 'attribute',
                'verbose_name_plural': 'attributes',
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
                ('structure', models.CharField(default=b'standalone', max_length=10, verbose_name='Product structure', choices=[(b'standalone', 'Stand-alone product'), (b'parent', 'Parent product'), (b'child', 'Child product')])),
                ('title', models.CharField(max_length=255, verbose_name='Product title', blank=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('is_recommended', models.BooleanField(default=False)),
                ('is_banner', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('category', models.ForeignKey(to='main.Category')),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='main.Cottage', help_text="Only choose a parent product if you're creating a child product.  For example if this is a size 4 of a particular t-shirt.  Leave blank if this is a stand-alone product (i.e. there is only one version of this product).", null=True, verbose_name='Parent product')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.ImageField(upload_to=b'')),
                ('entity_id', models.PositiveIntegerField()),
                ('entity_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
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
        migrations.AlterUniqueTogether(
            name='schemaforcategory',
            unique_together=set([('schema', 'category')]),
        ),
        migrations.AddField(
            model_name='choice',
            name='schema',
            field=models.ForeignKey(to='main.Schema'),
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
            field=models.ForeignKey(to='main.Choice'),
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
            field=models.ForeignKey(to='main.Schema'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='attribute',
            unique_together=set([('entity_type', 'entity_id', 'schema', 'choice')]),
        ),
    ]

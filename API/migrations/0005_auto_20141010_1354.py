# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_user_list_place'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_type', models.CharField(max_length=100)),
                ('flyer', models.CharField(max_length=100, null=True)),
                ('stock', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=400, null=True)),
                ('bar', models.ForeignKey(to='API.Bar')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('used_at', models.DateTimeField(null=True)),
                ('item', models.ForeignKey(to='API.Item', null=True)),
                ('owner', models.ForeignKey(to='API.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='pass',
            name='bar',
        ),
        migrations.RemoveField(
            model_name='pass',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Pass',
        ),
    ]

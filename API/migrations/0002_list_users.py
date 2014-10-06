# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='users',
            field=models.ManyToManyField(to='API.User'),
            preserve_default=True,
        ),
    ]

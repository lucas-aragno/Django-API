# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_auto_20141004_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='list_place',
            field=models.ForeignKey(to='API.List', null=True),
            preserve_default=True,
        ),
    ]

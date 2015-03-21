# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0011_auto_20150321_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='url',
            field=models.URLField(unique=True, max_length=2048),
            preserve_default=True,
        ),
    ]

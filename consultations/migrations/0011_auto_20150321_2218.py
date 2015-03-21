# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0010_auto_20150321_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='url',
            field=models.URLField(unique=True, max_length=4096),
            preserve_default=True,
        ),
    ]

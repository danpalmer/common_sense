# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0013_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='raw_text',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0004_auto_20150321_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='contact_email',
            field=models.EmailField(default=None, max_length=75),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='consultation',
            name='summary',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]

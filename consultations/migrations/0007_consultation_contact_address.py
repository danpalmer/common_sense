# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0006_auto_20150321_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='contact_address',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]

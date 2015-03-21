# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0008_auto_20150321_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultation',
            name='description',
        ),
    ]

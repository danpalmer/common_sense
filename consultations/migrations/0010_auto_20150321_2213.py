# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0009_remove_consultation_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='title',
            field=models.CharField(max_length=500),
            preserve_default=True,
        ),
    ]

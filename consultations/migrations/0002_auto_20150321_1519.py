# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultation',
            name='organisation',
        ),
        migrations.AlterField(
            model_name='consultation',
            name='description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]

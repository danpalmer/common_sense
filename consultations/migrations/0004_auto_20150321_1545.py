# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0003_consultation_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='url',
            field=models.URLField(unique=True),
            preserve_default=True,
        ),
    ]

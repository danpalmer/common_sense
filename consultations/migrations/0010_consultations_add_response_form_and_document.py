# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0009_remove_consultation_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='response_document',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consultation',
            name='response_form',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
    ]

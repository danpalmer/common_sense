# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0010_consultations_add_response_form_and_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='organisation',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consultation',
            name='organisation_abbr',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]

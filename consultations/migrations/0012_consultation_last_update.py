# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0011_consultations_add_organisation_and_abbr'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
    ]

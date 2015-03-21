# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import consultations.enums


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0002_auto_20150321_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='state',
            field=models.IntegerField(verbose_name=consultations.enums.ConsultationStateEnum, default=None),
            preserve_default=False,
        ),
    ]

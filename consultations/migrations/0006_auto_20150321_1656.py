# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0005_auto_20150321_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='contact_email',
            field=models.EmailField(max_length=75, blank=True),
            preserve_default=True,
        ),
    ]

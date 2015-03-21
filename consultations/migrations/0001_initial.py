# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('organisation', models.CharField(max_length=200)),
                ('closing_date', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

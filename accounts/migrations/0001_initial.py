# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('consultations', '0008_auto_20150321_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTopic',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('topic', models.ForeignKey(to='consultations.Topic', related_name='users')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='topics')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0007_consultation_contact_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultationTopic',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('consultation', models.ForeignKey(related_name='topics', to='consultations.Consultation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='consultationtopic',
            name='topic',
            field=models.ForeignKey(related_name='consultations', to='consultations.Topic'),
            preserve_default=True,
        ),
    ]

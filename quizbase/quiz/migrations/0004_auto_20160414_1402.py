# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20160407_1505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='correctness',
        ),
        migrations.AddField(
            model_name='answer',
            name='points',
            field=models.IntegerField(default=0, choices=[(2, b'Correct'), (1, b'Not Wrong'), (0, b'Incorrect')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_remove_quiz_attempt_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz_attempt',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='quiz_attempt',
            name='start_time',
        ),
        migrations.AddField(
            model_name='quiz_attempt',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]

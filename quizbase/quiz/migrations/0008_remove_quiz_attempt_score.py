# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_remove_answer_attempt_submit_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz_attempt',
            name='score',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20160414_1402'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='points',
            new_name='value',
        ),
    ]

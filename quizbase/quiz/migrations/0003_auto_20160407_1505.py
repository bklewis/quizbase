# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_remove_question_ord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]

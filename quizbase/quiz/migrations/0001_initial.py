# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('string', models.CharField(max_length=1000)),
                ('correctness', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Answer_attempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submit_time', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('answer', models.ForeignKey(to='quiz.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('string', models.CharField(max_length=1000)),
                ('ord', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz_attempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attempt_no', models.IntegerField()),
                ('score', models.IntegerField()),
                ('start_time', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('end_time', models.DateTimeField()),
                ('quiz', models.ForeignKey(to='quiz.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=500)),
                ('permissions', models.IntegerField()),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='quiz_attempt',
            name='user',
            field=models.ForeignKey(to='quiz.User'),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(to='quiz.Quiz'),
        ),
        migrations.AddField(
            model_name='answer_attempt',
            name='quiz_attempt',
            field=models.ForeignKey(to='quiz.Quiz_attempt'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='quiz.Question'),
        ),
    ]

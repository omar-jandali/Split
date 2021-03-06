# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-22 00:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0002_bundle_expense_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='some action', max_length=200)),
                ('host', models.CharField(max_length=100, null=True)),
                ('category', models.SmallIntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bundle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.Bundle')),
                ('expense', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.Expense')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

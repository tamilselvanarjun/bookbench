# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-04 23:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20171105_0514'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='picture',
            field=models.ImageField(default=b'bookdefault.png', upload_to=b''),
        ),
    ]

# Generated by Django 5.0.1 on 2024-01-07 22:50

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0003_comment_comment_myblog_comm_created_b0137e_idx'),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
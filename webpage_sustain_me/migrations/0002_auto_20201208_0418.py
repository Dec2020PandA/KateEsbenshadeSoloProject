# Generated by Django 2.2 on 2020-12-08 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpage_sustain_me', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='action',
            old_name='decription',
            new_name='description',
        ),
    ]

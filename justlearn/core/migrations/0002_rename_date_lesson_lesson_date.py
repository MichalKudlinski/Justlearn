# Generated by Django 4.0.8 on 2022-11-16 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='date',
            new_name='lesson_date',
        ),
    ]
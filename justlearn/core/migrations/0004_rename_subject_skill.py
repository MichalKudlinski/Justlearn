# Generated by Django 4.0.8 on 2022-10-29 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_subject_user_is_student_user_is_teacher_teacher_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subject',
            new_name='Skill',
        ),
    ]
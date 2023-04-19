# Generated by Django 4.1.5 on 2023-04-19 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_platform', '0003_alter_course_instructor'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')], default=2),
            preserve_default=False,
        ),
    ]
# Generated by Django 3.1.6 on 2021-02-23 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20210204_1933'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-created_on']},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ['-created_on']},
        ),
    ]

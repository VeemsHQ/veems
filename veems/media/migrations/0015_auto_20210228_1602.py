# Generated by Django 3.1.6 on 2021-02-28 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0014_auto_20210228_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='status',
            field=models.CharField(
                choices=[
                    ('draft', 'draft'),
                    ('uploaded', 'uploaded'),
                    ('processing', 'processing'),
                    ('processing_viewable', 'processing_viewable'),
                    ('completed', 'completed'),
                ],
                db_index=True,
                default='draft',
                max_length=20,
            ),
        ),
    ]

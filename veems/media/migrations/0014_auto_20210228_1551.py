# Generated by Django 3.1.6 on 2021-02-28 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0013_auto_20210223_2037'),
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
                    ('completed', 'completed'),
                ],
                db_index=True,
                default='draft',
                max_length=10,
            ),
        ),
    ]

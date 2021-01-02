from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_user_sync_videos_interested'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(
                max_length=254, unique=True, verbose_name='email address'
            ),
        ),
    ]

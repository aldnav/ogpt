# Generated by Django 2.2 on 2019-04-30 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('govproject', '0008_auto_20190427_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='governmentproject',
            name='removed',
            field=models.BooleanField(default=False, help_text='Mark project as removed'),
        ),
    ]

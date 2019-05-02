# Generated by Django 2.2 on 2019-05-02 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('govproject', '0012_auto_20190430_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='governmentproject',
            name='is_draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='governmentproject',
            name='media_files',
            field=models.ManyToManyField(blank=True, help_text='Attached media files to the project', related_name='projects', to='govproject.ProjectMedia'),
        ),
    ]
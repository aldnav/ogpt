# Generated by Django 2.2 on 2019-04-27 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('govproject', '0006_auto_20190427_0902'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_media', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='governmentproject',
            name='media_files',
            field=models.ManyToManyField(help_text='Attached media files to the project', related_name='projects', to='govproject.ProjectMedia'),
        ),
    ]

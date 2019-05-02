# Generated by Django 2.2 on 2019-04-30 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('govproject', '0011_progressreport_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progressreport',
            name='tags',
            field=models.ManyToManyField(blank=True, help_text='Optional tags', related_name='tags', to='govproject.Tag'),
        ),
    ]
# Generated by Django 2.1.5 on 2019-02-12 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0002_periodo_jornada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodo',
            name='jornada',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
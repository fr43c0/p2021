# Generated by Django 2.1.5 on 2019-02-12 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0006_remove_periodo_jornada_trab'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodo',
            name='jornada_t',
            field=models.TimeField(blank=True, null=True),
        ),
    ]

# Generated by Django 2.1.5 on 2019-02-16 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0021_auto_20190216_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodo',
            name='media_dias_t',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='periodo',
            name='media_h_d_c',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='periodo',
            name='media_h_d_t',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
# Generated by Django 2.1.5 on 2019-02-28 00:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ponto', '0031_periodo_display'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colaborador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='obs',
            name='display',
        ),
        migrations.RemoveField(
            model_name='obs',
            name='entrada',
        ),
        migrations.RemoveField(
            model_name='obs',
            name='saida',
        ),
    ]
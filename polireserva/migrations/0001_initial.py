# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-15 19:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mantenimiento',
            fields=[
                ('id_M', models.AutoField(primary_key=True, serialize=False)),
                ('date_c', models.DateField(verbose_name='Fecha de submicion')),
                ('kindM', models.CharField(choices=[('PRE', 'Preventivo'), ('COR', 'Correctivo')], default='Preventivo', max_length=10, verbose_name='Tipo de mantenimiento realizado')),
                ('reason', models.CharField(max_length=200, verbose_name='Razon del mantenimiento')),
                ('report', models.CharField(max_length=100, verbose_name='Reporte de finalizacion')),
                ('estado', models.CharField(choices=[('Encurso', 'Encurso'), ('Finalizado', 'Finalizado'), ('Enespera', 'Enespera')], default='Encurso', max_length=10, verbose_name='Estado del mantenimiento')),
            ],
        ),
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id_r', models.AutoField(primary_key=True, serialize=False, verbose_name='Codigo del item')),
                ('name_r', models.CharField(max_length=30, verbose_name='Nombre del item')),
                ('description', models.CharField(max_length=50, verbose_name='Descripcion del item')),
                ('status', models.CharField(choices=[('Disponible', 'Disponible'), ('EnUso', 'En Uso'), ('NoDisponible', 'No Disponible'), ('Mantenimiento', 'Mantenimiento')], default='Disponible', max_length=13, verbose_name='Estado')),
                ('date_c', models.DateField(verbose_name='Fecha de submicion')),
                ('date_m', models.DateField(verbose_name='Fecha de alteracion')),
            ],
        ),
        migrations.CreateModel(
            name='Reservas',
            fields=[
                ('id_R', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('ACT', 'Activa'), ('CAN', 'Cancelada'), ('FIN', 'Finalizada'), ('EC', 'Encurso')], default='Activa', max_length=10)),
                ('obs', models.CharField(max_length=100)),
                ('date_i', models.DateTimeField()),
                ('date_f', models.DateTimeField()),
                ('recursos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polireserva.Recurso')),
            ],
        ),
        migrations.CreateModel(
            name='TdRecurso',
            fields=[
                ('id_tdr', models.AutoField(primary_key=True, serialize=False, verbose_name='Codigo del Tipo de Recurso')),
                ('description', models.CharField(max_length=30, verbose_name='Descripcion del Tipo de Recurso')),
            ],
        ),
        migrations.AddField(
            model_name='reservas',
            name='tdr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polireserva.TdRecurso'),
        ),
        migrations.AddField(
            model_name='reservas',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recurso',
            name='id_tdr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polireserva.TdRecurso'),
        ),
        migrations.AddField(
            model_name='mantenimiento',
            name='recurso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polireserva.Recurso'),
        ),
        migrations.AddField(
            model_name='mantenimiento',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

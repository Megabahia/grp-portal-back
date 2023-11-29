# Generated by Django 3.1.7 on 2022-02-02 20:34

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonedasEmpresa',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('fechaCobro', models.DateField(auto_now_add=True, null=True)),
                ('numeroFactura', models.TextField(blank=True, max_length=255, null=True)),
                ('montoSupermonedas', models.FloatField(blank=True, null=True)),
                ('montoTotalFactura', models.FloatField(blank=True, null=True)),
                ('nombreCompleto', models.CharField(blank=True, max_length=255, null=True)),
                ('nombres', models.CharField(blank=True, max_length=255, null=True)),
                ('apellidos', models.CharField(blank=True, max_length=255, null=True)),
                ('identificacion', models.CharField(blank=True, max_length=10, null=True)),
                ('whatsapp', models.CharField(blank=True, max_length=20, null=True)),
                ('empresa_id', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('state', models.SmallIntegerField(default=1)),
            ],
        ),
    ]

# Generated by Django 3.1.7 on 2021-09-28 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('central_catalogo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogo',
            name='config',
            field=models.TextField(default='{}'),
        ),
    ]
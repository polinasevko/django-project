# Generated by Django 3.2.7 on 2021-10-29 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mainapp', '0013_auto_20211025_1838'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorySpec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specification', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='Validator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_value', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category')),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='specification.categoryspec')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSpec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.product')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='specification.categoryspec')),
            ],
        ),
    ]
# Generated by Django 4.2.19 on 2025-03-08 14:10

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
            name='Charger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('charger_id', models.CharField(max_length=50, unique=True)),
                ('model', models.CharField(max_length=50)),
                ('vendor', models.CharField(max_length=50)),
                ('status', models.CharField(default='Available', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('location', models.CharField(max_length=255, unique=True)),
                ('chargers', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('energy_consumed', models.FloatField(default=0.0)),
                ('charger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='api.charger')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StatusLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('charger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.charger')),
            ],
        ),
        migrations.AddField(
            model_name='charger',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.station'),
        ),
    ]

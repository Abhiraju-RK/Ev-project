# Generated by Django 5.0.4 on 2025-04-07 04:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='booking',
            name='slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.availableslot'),
        ),
        migrations.AddField(
            model_name='staff',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='station',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.staff'),
        ),
        migrations.AddField(
            model_name='availableslot',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.station'),
        ),
    ]

# Generated by Django 3.0.5 on 2020-04-22 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financial_planner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Funds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('type', models.CharField(max_length=20)),
                ('investment', models.DecimalField(decimal_places=3, default=0.0, max_digits=10)),
                ('choice', models.CharField(choices=[('WATCHLIST', 'W'), ('MAIN_PORTFOLIO', 'P')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10)),
                ('name', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('quantity_owned', models.IntegerField(default=0, max_length=10)),
                ('initial_price', models.DecimalField(decimal_places=3, default=0.0, max_digits=10)),
                ('choice', models.CharField(choices=[('WATCHLIST', 'W'), ('MAIN_PORTFOLIO', 'P')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]

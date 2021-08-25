# Generated by Django 3.2.6 on 2021-08-24 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('symbol', models.CharField(max_length=255)),
                ('code', models.IntegerField()),
                ('url', models.URLField()),
                ('indicators_url', models.URLField()),
                ('status', models.IntegerField(choices=[(1, 'Enable'), (0, 'Disable')], default=1)),
            ],
        ),
    ]
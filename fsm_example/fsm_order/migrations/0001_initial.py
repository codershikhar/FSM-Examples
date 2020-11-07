# Generated by Django 3.1.1 on 2020-11-05 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('product', models.CharField(max_length=200)),
                ('status', models.SmallIntegerField(choices=[(0, 'created'), (1, 'paid'), (2, 'fulfilled'), (3, 'cancelled'), (4, 'returned')], default=0)),
            ],
        ),
    ]

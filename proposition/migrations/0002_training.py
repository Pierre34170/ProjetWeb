# Generated by Django 3.0.3 on 2020-02-28 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('proposition', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_training', models.CharField(max_length=30)),
                ('date_training', models.DateTimeField()),
                ('type_training', models.CharField(max_length=300)),
                ('team_training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Team')),
            ],
        ),
    ]

# Generated by Django 3.1.1 on 2021-01-10 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20210107_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(choices=[('S', 'Specialist'), ('A', 'Analyst'), ('L', 'Leader')], default='S', max_length=10),
        ),
    ]

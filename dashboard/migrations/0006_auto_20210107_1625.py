# Generated by Django 3.1.1 on 2021-01-07 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20201229_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(choices=[('S', 'Specialist'), ('A', 'Analyst'), ('L', 'Leader')], default='S', max_length=10),
        ),
    ]

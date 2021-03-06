# Generated by Django 3.1.1 on 2020-12-29 21:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0004_auto_20201229_1151'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Specialist',
            new_name='Employee',
        ),
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['team'], 'verbose_name_plural': 'Employees'},
        ),
        migrations.AlterModelOptions(
            name='statistics',
            options={'ordering': ['employee'], 'verbose_name_plural': 'Statistics'},
        ),
        migrations.RenameField(
            model_name='qa_score',
            old_name='specialist',
            new_name='employee',
        ),
        migrations.RenameField(
            model_name='statistics',
            old_name='specialist',
            new_name='employee',
        ),
        migrations.RenameField(
            model_name='timestats',
            old_name='specialist',
            new_name='employee',
        ),
        migrations.AlterField(
            model_name='updates',
            name='important',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='qa_score',
            unique_together={('employee', 'qa_ticket')},
        ),
        migrations.AlterUniqueTogether(
            name='statistics',
            unique_together={('employee', 'date')},
        ),
    ]

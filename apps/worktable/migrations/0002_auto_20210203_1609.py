# Generated by Django 3.1.5 on 2021-02-03 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('worktable', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorderlog',
            name='record_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='worktable.workorder', verbose_name='单号'),
        ),
        migrations.AlterField(
            model_name='workorderlog',
            name='recorder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='记录人'),
        ),
    ]
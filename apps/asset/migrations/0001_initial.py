# Generated by Django 2.1 on 2021-01-20 08:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(blank=True, max_length=32, null=True, verbose_name='单号')),
                ('edp_asset', models.CharField(blank=True, max_length=64, null=True, verbose_name='电脑部资产')),
                ('target_asset', models.CharField(blank=True, max_length=64, null=True, verbose_name='目标部门资产')),
                ('transfer_time', models.DateTimeField(auto_now_add=True, verbose_name='转移时间')),
                ('remark', models.TextField(blank=True, default='', null=True, verbose_name='备注')),
                ('target_department', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.Department', verbose_name='目标部门')),
            ],
            options={
                'verbose_name': '资产管理',
                'verbose_name_plural': '资产管理',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=32, verbose_name='品牌')),
                ('model', models.CharField(max_length=32, verbose_name='型号')),
                ('parameter', models.CharField(blank=True, max_length=128, null=True, verbose_name='参数')),
                ('is_network', models.BooleanField(choices=[(True, '是'), (False, '否')], default=True, verbose_name='是否网络设备')),
            ],
            options={
                'verbose_name': '属性信息',
                'verbose_name_plural': '属性信息',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=32, unique=True, verbose_name='设备名')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, unique=True, verbose_name='IP地址')),
                ('login_name', models.CharField(blank=True, max_length=32, null=True, verbose_name='登录名')),
                ('login_pwd', models.CharField(blank=True, max_length=32, null=True, verbose_name='登录密码')),
                ('remark', models.TextField(blank=True, default='', null=True, verbose_name='备注信息')),
                ('asset_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='network_asset_user', to=settings.AUTH_USER_MODEL, verbose_name='使用人')),
            ],
            options={
                'verbose_name': '网络设备',
                'verbose_name_plural': '网络设备',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='OtherDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.TextField(blank=True, default='', null=True, verbose_name='备注信息')),
                ('asset_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='other_asset_user', to=settings.AUTH_USER_MODEL, verbose_name='使用人')),
            ],
            options={
                'verbose_name': '其它设备',
                'verbose_name_plural': '其它设备',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='RecordLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_time', models.DateTimeField(auto_now_add=True, verbose_name='记录时间')),
                ('record_type', models.CharField(choices=[('create', '创建'), ('update', '修改'), ('transfer', '转移'), ('scrap', '报废')], default='create', max_length=16, verbose_name='记录类型')),
                ('remark', models.TextField(default='', verbose_name='内容')),
            ],
            options={
                'verbose_name': '记录日志',
                'verbose_name_plural': '记录日志',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('it_num', models.CharField(max_length=32, verbose_name='EDP编号')),
                ('acc_num', models.CharField(blank=True, max_length=32, null=True, verbose_name='ACC编号')),
                ('sn', models.CharField(max_length=32, verbose_name='序列号')),
                ('mac', models.CharField(blank=True, max_length=32, null=True, verbose_name='MAC地址')),
                ('rmb', models.IntegerField(blank=True, null=True, verbose_name='人民币')),
                ('hkd', models.IntegerField(blank=True, null=True, verbose_name='港币')),
                ('buy_date', models.DateField(blank=True, null=True, verbose_name='购买日期')),
                ('warranty_date', models.DateField(blank=True, null=True, verbose_name='到保日期')),
                ('state', models.CharField(choices=[('free', '闲置'), ('used', '在用'), ('disuse', '弃用'), ('scrap', '报废')], default='free', max_length=8, verbose_name='资产状态')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stock_department', to='users.Department', verbose_name='库存部门')),
                ('model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset.Attribute', verbose_name='型号')),
            ],
            options={
                'verbose_name': '库存信息',
                'verbose_name_plural': '库存信息',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TypeCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('simple_code', models.CharField(max_length=32, unique=True, verbose_name='简写分类')),
                ('en_code', models.CharField(max_length=32, verbose_name='英文分类')),
                ('cn_code', models.CharField(max_length=32, verbose_name='中文分类')),
            ],
            options={
                'verbose_name': '分类编码',
                'verbose_name_plural': '分类编码',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='recordlog',
            name='record_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.Stock', verbose_name='记录对象'),
        ),
        migrations.AddField(
            model_name='recordlog',
            name='recorder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asset_recorder', to=settings.AUTH_USER_MODEL, verbose_name='记录人'),
        ),
        migrations.AddField(
            model_name='otherdevice',
            name='stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset.Stock', verbose_name='设备编号'),
        ),
        migrations.AddField(
            model_name='networkdevice',
            name='stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='asset.Stock', verbose_name='设备编号'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='asset.TypeCode', verbose_name='分类'),
        ),
    ]

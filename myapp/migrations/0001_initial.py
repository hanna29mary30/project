# Generated by Django 3.1.6 on 2021-02-18 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ask_expert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ask_exid', models.IntegerField()),
                ('expert_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('questn', models.CharField(max_length=200)),
                ('answr', models.CharField(max_length=200)),
                ('date', models.CharField(max_length=200)),
                ('time', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='crop_master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cp_id', models.IntegerField()),
                ('cp_type', models.CharField(max_length=200)),
                ('scfc_name', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=200)),
                ('descp', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='crop_master_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpd_id', models.IntegerField()),
                ('cp_id', models.IntegerField()),
                ('cp_variety', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=200)),
                ('descp', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='cultivation_master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cul_id', models.IntegerField()),
                ('expert_id', models.IntegerField()),
                ('cp_id', models.CharField(max_length=200)),
                ('land_type', models.CharField(max_length=500)),
                ('soil_conc', models.CharField(max_length=200)),
                ('descp', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='disease_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_id', models.IntegerField()),
                ('expert_id', models.IntegerField()),
                ('cp_id', models.CharField(max_length=200)),
                ('d_type', models.CharField(max_length=200)),
                ('descp', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='expert_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expert_id', models.IntegerField()),
                ('fname', models.CharField(max_length=200)),
                ('lname', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('contact', models.IntegerField()),
                ('email', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fd_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('date', models.CharField(max_length=200)),
                ('time', models.CharField(max_length=300)),
                ('descp', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='fertilizer_master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_id', models.IntegerField()),
                ('expert_id', models.IntegerField()),
                ('f_type', models.CharField(max_length=200)),
                ('f_tittle', models.CharField(max_length=200)),
                ('descp', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=500)),
                ('status', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='pesticides_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pt_id', models.IntegerField()),
                ('expert_id', models.IntegerField()),
                ('pt_type', models.CharField(max_length=200)),
                ('cmp_name', models.CharField(max_length=500)),
                ('image', models.CharField(max_length=200)),
                ('descp', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='user_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('kcno', models.IntegerField()),
                ('fname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=25)),
                ('age', models.IntegerField()),
                ('addr', models.CharField(max_length=500)),
                ('pin', models.IntegerField()),
                ('contact', models.IntegerField()),
                ('email', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='user_login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=100)),
                ('passwd', models.CharField(max_length=25)),
                ('u_type', models.CharField(max_length=10)),
            ],
        ),
    ]
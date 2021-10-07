# Generated by Django 3.2.7 on 2021-10-05 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parents',
            fields=[
                ('parents_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('parents_pw', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'parents',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('subject_start', models.DateTimeField()),
                ('subject_finish', models.DateTimeField()),
            ],
            options={
                'db_table': 'timetable',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50)),
                ('user_age', models.IntegerField()),
                ('user_sex', models.IntegerField()),
                ('user_class', models.IntegerField()),
                ('grade', models.IntegerField()),
                ('parents_id', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserConc',
            fields=[
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('day_conc', models.DateField()),
                ('subject', models.CharField(max_length=100)),
                ('total_subject_time_conc', models.IntegerField()),
                ('eye_close_time', models.IntegerField()),
                ('not_seat_time', models.IntegerField()),
                ('total_conc_time', models.IntegerField()),
            ],
            options={
                'db_table': 'user_conc',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserEmotion',
            fields=[
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('day_emo', models.DateField()),
                ('subject', models.CharField(max_length=100)),
                ('sub_emotion', models.IntegerField()),
                ('sub_emotion_time', models.IntegerField()),
            ],
            options={
                'db_table': 'user_emotion',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.user')),
                ('filename', models.CharField(max_length=25)),
                ('emotion', models.IntegerField()),
                ('emotion_prob', models.FloatField()),
                ('is_eyeopen', models.IntegerField()),
                ('is_seat', models.IntegerField()),
            ],
            options={
                'db_table': 'frame',
                'managed': False,
            },
        ),
    ]
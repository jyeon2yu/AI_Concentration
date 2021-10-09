from django.db import models


class Frame(models.Model):
    user = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    filename = models.CharField(max_length=25)
    emotion = models.IntegerField()
    emotion_prob = models.FloatField()
    is_eyeopen = models.IntegerField()
    is_seat = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'frame'
        unique_together = (('user', 'filename'),)


class Parents(models.Model):
    parents_id = models.CharField(primary_key=True, max_length=100)
    parents_pw = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parents'


class Timetable(models.Model):
    class_field = models.IntegerField(db_column='class', primary_key=True)  # Field renamed because it was a Python reserved word.  
    subject = models.CharField(max_length=100)
    subject_day = models.IntegerField()
    subject_start_time = models.TimeField()
    subject_finish_time = models.TimeField()
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'timetable'
        unique_together = (('class_field', 'subject', 'subject_day', 'user'), ('subject_day', 'subject_start_time', 'subject_finish_time'),)


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=50)
    user_age = models.IntegerField()
    user_sex = models.IntegerField()
    user_class = models.IntegerField()
    parents_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserConc(models.Model):
    user = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    day_conc = models.DateField()
    subject = models.CharField(max_length=100)
    total_subject_time_conc = models.IntegerField()
    eye_close_time = models.IntegerField()
    not_seat_time = models.IntegerField()
    total_conc_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_conc'
        unique_together = (('user', 'day_conc', 'subject'),)


class UserEmotion(models.Model):
    user = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    day_emo = models.DateField()
    subject = models.CharField(max_length=100)
    sub_emotion = models.IntegerField()
    sub_emotion_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_emotion'
        unique_together = (('user', 'day_emo', 'subject', 'sub_emotion'),)


class Images(models.Model):
    image_name = models.CharField(primary_key=True, max_length=50)
    url = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'images'

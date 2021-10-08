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
        db_table = 'f   rame'
        unique_together = (('user', 'filename'),)

class Parents(models.Model):
    parents_id = models.CharField(primary_key=True, max_length=100)
    parents_pw = models.CharField(max_length=100, blank=True, null=True)      

    class Meta:
        managed = False
        db_table = 'parents'


class Timetable(models.Model):
    subject = models.CharField(max_length=100)
    subject_start = models.DateTimeField()
    subject_finish = models.DateTimeField()
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'timetable'


class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    user_name = models.CharField(max_length=50)
    user_age = models.IntegerField()
    user_sex = models.IntegerField()
    user_class = models.IntegerField()
    grade = models.IntegerField()
    parents_id = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'user'


class UserConc(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    day_conc = models.DateField()
    subject = models.CharField(max_length=100)
    total_subject_time_conc = models.IntegerField()
    eye_close_time = models.IntegerField()
    not_seat_time = models.IntegerField()
    total_conc_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_conc'
        unique_together = (('user_id', 'day_conc', 'subject'),)


class UserEmotion(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    day_emo = models.DateField()
    subject = models.CharField(max_length=100)
    sub_emotion = models.IntegerField()
    sub_emotion_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_emotion'
        unique_together = (('user_id', 'day_emo', 'subject', 'sub_emotion'),)

# 이미지 테이블 추가
class Images(models.Model):
    image_name = models.CharField(primary_key=True, max_length=50)
    url = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'images'

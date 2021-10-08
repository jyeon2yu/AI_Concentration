import collections
from typing import Collection
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms import model_to_dict


# 테이블, 쿼리셋 library
from app.models import User,UserConc,UserEmotion,Parents,Timetable,Images
from django.db.models import Sum, Count, Q, Max

from datetime import datetime, timedelta, date

import random
import sys, os
import json
import numpy as np


import cv2
from imutils import face_utils

import warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Create your views here.
def webcam(request):
    # return HttpResponse('Hello, webcam!')

    temp = 0
    content = {'temp':temp}

    return render(request, 'app/webcam.html', content)

# 이미지 url 가져오는 함수
def img_url():
    # images url
    url = Images.objects.filter(Q(image_name__startswith='emo'))
    url_list = {}
    for i in url:
        url_list.update({i.image_name:i.url})
    
    return url_list



    url_list = img_url()
    userID = userID
    today = todate # test data

    # 3-1. today daily emotion top 3
    today_emo = UserEmotion.objects.filter(user_id=userID, day_emo='2021-09-27').values('sub_emotion').annotate(time=Sum('sub_emotion_time')) # today emotion top3
    today_emo_list = []

    for data in today_emo:
        today_emo_list.append([data['sub_emotion'], data['time']])

    today_emo_list = sorted(today_emo_list, key=lambda x: (-x[1], x[0]))[:3] # today emotion top3

    # 3-2. today daily subject emotion top2
    useremotion = UserEmotion.objects.filter(user_id=userID, day_emo=today).order_by('subject','-sub_emotion_time')

    # img_info {
    #   'date' : '2021-09-27',
    #   'korean' : [[emo_3,url],.....], # order by decending
    #   ......
    # }
    # dictionary expression : {key: value for key, value in dict.fromkeys(keys).items()}
    img_info = {'date': today, 'korean': [], 'math': [], 'english': [], 'science': [], 'today_emo' : today_emo_list,}
    img_info['date'] = useremotion[0].day_emo



        # get each subject's emotion time
        if i.subject == 'korean':
            img_info['korean'].append([i.sub_emotion, i.sub_emotion_time])
            # get each emotion's total time
        elif i.subject == 'math':
            img_info['math'].append([i.sub_emotion, i.sub_emotion_time])
        elif i.subject == 'english':
            img_info['english'].append([i.sub_emotion, i.sub_emotion_time])
        else:
            img_info['science'].append([i.sub_emotion, i.sub_emotion_time])
    
    # today's top 3 emotion by each subject
    img_info['korean'] = sorted(img_info['korean'], key=lambda x: (-x[1], x[0]))[:3]
    img_info['math'] = sorted(img_info['math'], key=lambda x: (-x[1], x[0]))[:3]
    img_info['english'] = sorted(img_info['english'], key=lambda x: (-x[1], x[0]))[:3]
    img_info['science'] = sorted(img_info['science'], key=lambda x: (-x[1], x[0]))[:3]

     # paste url
    for key,value in img_info.items():
        # print(info['result'])
        if key in ['korean','math','english','science','today_emo']:
            for index, val in enumerate(value):
                if val[0] == 0:
                    val[0] = '중립'
                    val.append(url_list['emo_0'])
                elif val[0] == 1:
                    val[0] = '슬픔'
                    val.append(url_list['emo_1'])
                elif val[0] == 2:
                    val[0] = '상처'
                    val.append(url_list['emo_2'])
                elif val[0] == 3:
                    val[0] = '불안'
                    val.append(url_list['emo_3'])
                elif val[0] == 4:
                    val[0] = '분노'
                    val.append(url_list['emo_4'])
                elif val[0] == 5:
                    val[0] = '당황'
                    val.append(url_list['emo_5'])
                else :
                    val[0] = '기쁨'
                    val.append(url_list['emo_6'])


def subject_data(request) :

    english = model_to_dict(UserEmotion.objects.filter(user_id='1234').filter(day_emo='2021-09-27').filter(subject='english').order_by('-sub_emotion_time')[0])
    korean = model_to_dict(UserEmotion.objects.filter(user_id='1234').filter(day_emo='2021-09-27').filter(subject='korean').order_by('-sub_emotion_time')[0])
    math = model_to_dict(UserEmotion.objects.filter(user_id='1234').filter(day_emo='2021-09-27').filter(subject='math').order_by('-sub_emotion_time')[0])
    science = model_to_dict(UserEmotion.objects.filter(user_id='1234').filter(day_emo='2021-09-27').filter(subject='science').order_by('-sub_emotion_time')[0])

    emotions = [ english['sub_emotion'], korean['sub_emotion'], math['sub_emotion'], science['sub_emotion']]
    
    english_conc = model_to_dict(UserConc.objects.filter(user_id='1234').filter(day_conc='2021-09-27').filter(subject='english').get())
    korean_conc = model_to_dict(UserConc.objects.filter(user_id='1234').filter(day_conc='2021-09-27').filter(subject='korean').get())
    math_conc = model_to_dict(UserConc.objects.filter(user_id='1234').filter(day_conc='2021-09-27').filter(subject='math').get())
    science_conc = model_to_dict(UserConc.objects.filter(user_id='1234').filter(day_conc='2021-09-27').filter(subject='science').get())

    conc = []

    for t in [ english_conc, korean_conc, math_conc, science_conc] :
        if t['total_conc_time'] / t['total_subject_time_conc'] >= 0.7 :
            conc.append(1)
        elif t['total_conc_time'] / t['total_subject_time_conc'] >= 0.6 :
            conc.append(2)
        elif t['total_conc_time'] / t['total_subject_time_conc'] >= 0.5 :
            conc.append(3)
        elif t['total_conc_time'] / t['total_subject_time_conc'] >= 0.4 :
            conc.append(4)
        else :
            conc.append(5)
    
    data = {'emotions' : emotions, 'conc' : conc}
    return JsonResponse(data, safe=False)

# 과목 탭 1주
def subject_data_week(request) :
    emotions = []
    temp = [0] * 7
    english = UserEmotion.objects.filter(user_id='1234').filter(day_emo__gte='2021-09-27', day_emo__lte='2021-09-29').filter(subject='english')
    
    for d in english :
        temp[model_to_dict(d)['sub_emotion']] += model_to_dict(d)['sub_emotion_time']
    emotions.append(int(np.argmax(np.array(temp))))

    temp = [0] * 7
    korean = UserEmotion.objects.filter(user_id='1234').filter(day_emo__gte='2021-09-27', day_emo__lte='2021-09-29').filter(subject='korean')
    for d in korean :
        temp[model_to_dict(d)['sub_emotion']] += model_to_dict(d)['sub_emotion_time']
    emotions.append(int(np.argmax(np.array(temp))))

    temp = [0] * 7
    math = UserEmotion.objects.filter(user_id='1234').filter(day_emo__gte='2021-09-27', day_emo__lte='2021-09-29').filter(subject='math')
    for d in math :
        temp[model_to_dict(d)['sub_emotion']] += model_to_dict(d)['sub_emotion_time']
    emotions.append(int(np.argmax(np.array(temp))))

    temp = [0] * 7
    science = UserEmotion.objects.filter(user_id='1234').filter(day_emo__gte='2021-09-27', day_emo__lte='2021-09-29').filter(subject='science')
    for d in science :
        temp[model_to_dict(d)['sub_emotion']] += model_to_dict(d)['sub_emotion_time']
    emotions.append(int(np.argmax(np.array(temp))))


    english_conc = UserConc.objects.filter(user_id='1234').filter(day_conc__gte='2021-09-27', day_conc__lte='2021-09-29').filter(subject='english')
    korean_conc = UserConc.objects.filter(user_id='1234').filter(day_conc__gte='2021-09-27', day_conc__lte='2021-09-29').filter(subject='korean')
    math_conc = UserConc.objects.filter(user_id='1234').filter(day_conc__gte='2021-09-27', day_conc__lte='2021-09-29').filter(subject='math')
    science_conc = UserConc.objects.filter(user_id='1234').filter(day_conc__gte='2021-09-27', day_conc__lte='2021-09-29').filter(subject='science')

    conc = []

    for t in [english_conc, korean_conc, math_conc, science_conc] :
        if t.aggregate(Sum('total_conc_time'))['total_conc_time__sum'] / t.aggregate(Sum('total_subject_time_conc'))['total_subject_time_conc__sum'] >= 0.7 :
            conc.append(1)
        elif t.aggregate(Sum('total_conc_time'))['total_conc_time__sum'] / t.aggregate(Sum('total_subject_time_conc'))['total_subject_time_conc__sum'] >= 0.6 :
            conc.append(2)
        elif t.aggregate(Sum('total_conc_time'))['total_conc_time__sum'] / t.aggregate(Sum('total_subject_time_conc'))['total_subject_time_conc__sum'] >= 0.5 :
            conc.append(3)
        elif t.aggregate(Sum('total_conc_time'))['total_conc_time__sum'] / t.aggregate(Sum('total_subject_time_conc'))['total_subject_time_conc__sum'] >= 0.4 :
            conc.append(4)
        else :
            conc.append(5)

    data = {'emotions' : emotions, 'conc' : conc}
    
    return JsonResponse(data, safe=False)

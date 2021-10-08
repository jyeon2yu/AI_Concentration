import collections
from typing import Collection
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms import model_to_dict
from django.db.models import Sum
from app.models import User,UserConc,UserEmotion,Parents,Timetable

import datetime
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


def report_chart(request):
    # get userconc data order by date
    userconc = UserConc.objects.filter(user_id='1234').order_by('day_conc','subject')
    user = User.objects.get(user_id='1234')

    content = {'user_info':user, 'week':[]}

    # set info dictionary
    content['week'].append(userconc[0].day_conc)
    for i in userconc:
        # get date
        if i.day_conc != content['week'][-1]:
            content['week'].append(i.day_conc)

    
    return render(request, 'chart.html', content)

@csrf_exempt
def report_data(request):

    # info {'week':[2021-09-27,...],
    #       'korean': [[total_subject_time_conc, total_conc_time],[],...], 
    #        ...,
    #       'result' : [(ko+ma+en+sci/total_time), ... ]}
    info = {'week':[], 'korean':[], 'math': [], 'english':[], 'science': [], 'time': [], 'result':[]}
    jsonObject = json.loads(request.body)


    # get userconc data order by date
    userconc = UserConc.objects.filter(user_id='1234').order_by('day_conc','subject')

    # set info dictionary
    info['week'].append(userconc[0].day_conc)
    for i in userconc:
        # get date
        if i.day_conc != info['week'][-1]:
            info['week'].append(i.day_conc)

        # get each subject's conc time
        if i.subject == 'korean':
            info['korean'].append([i.total_subject_time_conc, i.total_conc_time])
        elif i.subject == 'math':
            info['math'].append([i.total_subject_time_conc, i.total_conc_time])
        elif i.subject == 'english':
            info['english'].append([i.total_subject_time_conc, i.total_conc_time])
        else:
            info['science'].append([i.total_subject_time_conc, i.total_conc_time])
    

    # print(info)

    # calculation a conc's result
    info['result'] = [0 for i in range(len(info['week']))]
    info['time'] = [0 for i in range(len(info['week']))]
    for key,value in info.items():
        # print(info['result'])
        if key in ['korean','math','english','science']:
            for index, val in enumerate(value):
                # print(index, val)
                info['time'][index] += val[0]
                info['result'][index] += val[1]

    # send data
    return JsonResponse(info)


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

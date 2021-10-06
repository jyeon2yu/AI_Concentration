from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms import model_to_dict
from app.models import User,UserConc,UserEmotion,Parents,Timetable

import datetime
import random
import sys, os
import json

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
    
    print('Views.subject_data')
    data = UserEmotion.objects.filter(user_id='1234').filter(day_emo='2021-09-27').order_by('subject')
    
    emotions = []
    for d in data :
        emotions.append(model_to_dict(d)['sub_emotion'])

    print(data)
    return JsonResponse(emotions, safe=False)
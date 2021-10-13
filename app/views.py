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
from operator import itemgetter
from pytz import timezone

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

# 하루 집중도 데이터 가져오는 함수
def daily_conc(userID, today):

    info = {'today_conc':{}, 'korean': {}, 'math': {}, 'english':{}, 'science':{}}

    todate = today
    userid = userID
    today_conc = UserConc.objects.filter(user_id=userid, day_conc=todate).annotate(total_subject=Sum('total_subject_time_conc'),
    eye_close=Sum('eye_close_time'), not_seat=Sum('not_seat_time'), conc_time=Sum('total_conc_time'))

    info['today_conc']['eye_close'] = round(today_conc[0].eye_close / today_conc[0].total_subject * 100, 2) # 눈 감은 시간
    info['today_conc']['not_seat'] = round(today_conc[0].not_seat / today_conc[0].total_subject * 100, 2) # 자리 이석 시간
    info['today_conc']['conc_time'] = round(today_conc[0].conc_time / today_conc[0].total_subject * 100, 2) # 집중한 시간

    subject_list = ['korean', 'math', 'english', 'science']
    for subject in subject_list:
        subject_conc = UserConc.objects.filter(user_id=userid, day_conc=todate, subject=subject)

        info[subject]['eye_close'] = round(subject_conc[0].eye_close_time / subject_conc[0].total_subject_time_conc * 100, 2) # 눈 감은 시간
        info[subject]['not_seat'] = round(subject_conc[0].not_seat_time / subject_conc[0].total_subject_time_conc * 100, 2) # 자리 이석 시간
        info[subject]['conc_time'] = round(subject_conc[0].total_conc_time / subject_conc[0].total_subject_time_conc * 100, 2) # 집중한 시간

    return info

# 하루 감정 데이터 가져오는 함수
def daily_emotion(userID, todate):

    url_list = img_url()
    userid = userID
    today = todate # test data

    # 3-1. today daily emotion top 3
    today_emo = UserEmotion.objects.filter(user_id=userid, day_emo='2021-09-27').values('sub_emotion').annotate(time=Sum('sub_emotion_time')) # today emotion top3
    today_emo_list = []

    for data in today_emo:
        today_emo_list.append([data['sub_emotion'], data['time']])

    today_emo_list = sorted(today_emo_list, key=lambda x: (-x[1], x[0]))[:3] # today emotion top3

    # 3-2. today daily subject emotion top2
    useremotion = UserEmotion.objects.filter(user_id=userid, day_emo=today).order_by('subject','-sub_emotion_time')

    # img_info {
    #   'date' : '2021-09-27',
    #   'korean' : [[emo_3,url],.....], # order by decending
    #   ......
    # }
    # dictionary expression : {key: value for key, value in dict.fromkeys(keys).items()}
    img_info = {'date': today, 'korean': [], 'math': [], 'english': [], 'science': [], 'today_emo' : today_emo_list,}
    img_info['date'] = useremotion[0].day_emo

    for i in useremotion:

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

    return img_info

# 등급 선정하는 함수
def getGrade(conc,total):
    if total == 0:
        return False
    conc_per = conc/total
    if conc_per >= 0.9:
        return 1
    elif conc_per >= 0.8:
        return 2
    elif conc_per >= 0.6:
        return 3
    elif conc_per >= 0.8:
        return 4
    else:
        return 5

# "chart.html"
def report_chart(request):

    content = {'user_info':{}, 'week':[]}

    ### 1. Set User Info
    # get userconc data order by date
    user = User.objects.get(user_id='1234')
    content['user_info'] = user
    

    ### 2. Set Date Info
    date = []
    todate = datetime.now()
    today = datetime.now().weekday() # 오늘 요일

    # 오늘 날짜
    day = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    date.append([ todate.strftime('%Y-%m-%d'), day[today] ])

    # 월요일 찾기
    newdate = todate - timedelta(days=today)
    if today != 0:
        date.append(newdate.strftime('%Y-%m-%d'))
    else:
        date.append(todate.strftime('%Y-%m-%d'))

    # 금요일 찾기
    date.append((datetime.strptime(date[0][0], '%Y-%m-%d') + timedelta(days=4)).strftime('%Y-%m-%d'))

    content['week'] = date

    ### 3. Set Daily Emotion Info
    # 3-1. today daily emotion top 3
    today = '2021-09-27' # test data
    content['daily_emotion'] = daily_emotion(1234, today)
    # content.update(daily_conc(1234, today))
    content['daily_conc'] = daily_conc(1234,today)

    
    return render(request, 'chart.html', content)

# 과목 탭 1일
def subject_data(request) :
    
    # print('Views.subject_data')

    english = model_to_dict(UserEmotion.objects.filter(user_id='1234').filter(day_emo='2021-09-27').filter(subject='english').order_by('-sub_emotion_time')[0])
    korean = model_to_dict(UserEmotion.objects.filter(user_id='1234').filter(day_emo='2021-09-27').filter(subject='korean').order_by('-sub_emotion_time')[0])
    math = model_to_dict(UserEmotion.objects.filter(user_id='1234').filter(day_emo='2021-09-27').filter(subject='math').order_by('-sub_emotion_time')[0])
    science = model_to_dict(UserEmotion.objects.filter(user_id='1234').filter(day_emo='2021-09-27').filter(subject='science').order_by('-sub_emotion_time')[0])

    emotions = [ english['sub_emotion'], korean['sub_emotion'], math['sub_emotion'], science['sub_emotion']]
    
    # print('emotions', emotions)
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
    # print("\n\n 1주\n\n")
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


    # print('\n1주 끝\n')
    data = {'emotions' : emotions, 'conc' : conc}
    
    return JsonResponse(data, safe=False)

def conc_daily(request):

    info = daily_conc(1234, '2021-09-27')
    
    return JsonResponse(info)


@csrf_exempt
def conc_week(request):

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
    info['result'] = [0 for i in range(len(info['week']))] # Total class hours by date (total_subject_time sum)
    info['time'] = [0 for i in range(len(info['week']))] # Total intensive time by date and subject (total_conc_time sum)
    for key,value in info.items():
        # print(info['result'])
        if key in ['korean','math','english','science']:
            for index, val in enumerate(value):
                # print(index, val)
                info['time'][index] += val[0]
                info['result'][index] += val[1]

    # send data
    return JsonResponse(info)

@csrf_exempt
def emotion_daily(request):

    ### 1. set a data
    today = '2021-09-27' # test data
    
    ### 2. call a function
    url_list = img_url()
    daily_info = daily_emotion('1234', today)

    return JsonResponse(daily_info)

@csrf_exempt
def emotion_week(request):
     ### images url
    url = Images.objects.filter(Q(image_name__startswith='emo'))
    url_list = {}
    for i in url:
        url_list.update({i.image_name:i.url})

    ### get today's data
    # todate = datetime.datetime.now().strftime('%Y-%m-%d') # 오늘날짜
    date = []
    todate = datetime.now()
    today = datetime.now().weekday() # 오늘 요일

    # 월요일 찾기
    if today != 0:
        newdate = todate - timedelta(days=today)
        date.append(newdate.strftime('%Y-%m-%d'))
    else:
        date.append(todate.strftime('%Y-%m-%d'))

    # 금요일 찾기
    if today != 4:
        newdate = todate + timedelta(days=(4-today))
        date.append(newdate.strftime('%Y-%m-%d'))
    else:
        date.append(todate.strftime('%Y-%m-%d'))

    week_info = {'week_emo':[], 'korean':[], 'math':[], 'english':[], 'science':[]}


    temp = datetime(2021,9,27)
    for i in range(5):
        week_info['week_emo'].append([UserEmotion.objects.filter(user_id='1234', day_emo=temp).values('sub_emotion').annotate(time=Sum('sub_emotion_time')).order_by('-time')[0]['sub_emotion']])
        week_info['korean'].append([UserEmotion.objects.filter(user_id='1234', day_emo=temp, subject='korean').values('sub_emotion').annotate(time=Max('sub_emotion_time')).order_by('-time')[0]['sub_emotion']])
        week_info['math'].append([UserEmotion.objects.filter(user_id='1234', day_emo=temp, subject='math').values('sub_emotion').annotate(time=Max('sub_emotion_time')).order_by('-time')[0]['sub_emotion']])
        week_info['english'].append([UserEmotion.objects.filter(user_id='1234', day_emo=temp, subject='english').values('sub_emotion').annotate(time=Max('sub_emotion_time')).order_by('-time')[0]['sub_emotion']])
        week_info['science'].append([UserEmotion.objects.filter(user_id='1234', day_emo=temp, subject='science').values('sub_emotion').annotate(time=Max('sub_emotion_time')).order_by('-time')[0]['sub_emotion']])

        temp = temp + timedelta(days=1)

    
    # paste url
    for value in week_info.values():
        # print(info['result'])
        for val in value:
            if val[0] == 0:
                val.append('중립')
                val.append(url_list['emo_0'])
            elif val[0] == 1:
                val.append('슬픔')
                val.append(url_list['emo_1'])
            elif val[0] == 2:
                val.append('상처')
                val.append(url_list['emo_2'])
            elif val[0] == 3:
                val.append('불안')
                val.append(url_list['emo_3'])
            elif val[0] == 4:
                val.append('분노')
                val.append(url_list['emo_4'])
            elif val[0] == 5:
                val.append('당황')
                val.append(url_list['emo_5'])
            else :
                val.append('기쁨')
                val.append(url_list['emo_6'])

    return JsonResponse(week_info)

@csrf_exempt
def home(request):
    ### 1. set a data
    today = '2021-10-10' # test data
    user_id = '1234'

    #cal
    conc = UserConc.objects.filter(Q(user_id = user_id)&Q(day_conc = today)).annotate(conc_time=Sum('total_conc_time'),total_time=Sum('total_subject_time_conc')).values('conc_time','total_time')[0]
    emotion = UserEmotion.objects.filter(Q(user_id = user_id)&Q(day_emo = today)).values('sub_emotion').annotate(emo_time=Sum('sub_emotion_time')).order_by('-emo_time')[0]
 
    todays_conc = getGrade(conc['conc_time'], conc['total_time'])

    todays_emo_url = Images.objects.filter(image_name = 'emo_'+str(emotion['sub_emotion']))[0].url
    todays_conc_url = Images.objects.filter(image_name = 'grade_'+str(todays_conc))[0].url

    best_shot = Images.objects.filter(image_name__startswith = user_id).order_by('-image_name')[0]

    data = {'todays_conc':todays_conc_url, 'todays_emo' : todays_emo_url, 'best_shot' : best_shot.url}

    return JsonResponse(data)
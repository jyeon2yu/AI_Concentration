from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from mysql import DB
from django.contrib import messages
from app.models import Parents, User, Timetable
from django.views.decorators.csrf import csrf_exempt

from django.core.exceptions import ObjectDoesNotExist
import datetime

# Create your views here.
def login(request):

    if request.method == "POST":
        print(request.POST)
        parents_id = request.POST['uid']
        parents_pw = request.POST['upw']
        try:
            member = Parents.objects.get(parents_id=parents_id)
            if (member.parents_id == parents_id) & (member.parents_pw == parents_pw):
                request.session['uid'] = member.parents_id

                return render(request, 'user/check_user.html')
            else :
                return redirect('/')
        
        except Parents.DoesNotExist:
            messages.error(request, "로그인 실패")
            return redirect('/')
    
    # request.method == "GET"
    else:
        return render(request, 'user/login.html')


def check_user(request):
    
    if request.method == "POST":
        print("check_user POST: ", request.POST)
        request.session['cid'] = request.POST.get('user_id')
        return redirect('/app/report')
    else:
        children = User.objects.filter(parents_id=request.session['uid'])
        content = {}
        for data in children:
            content[data.user_id] = data.user_name

        return JsonResponse(content)

def logout(request):
    if request.session.get('uid'):
        del(request.session['uid'])
    return redirect('/')



def signup(request):
    if request.method=="POST":
        # print(request.POST.get('signup_class').__class__)
        try:
            parents = Parents.objects.get(parents_id=request.POST.get('signup_uid'))

            return render(request, 'user/signup.html')
            # return redirect('signup')

        except Parents.DoesNotExist:
            new_user = Parents(parents_id=request.POST.get('signup_uid'), parents_pw=request.POST.get('signup_upw'))

            index = User.objects.last()
            index = index.user_id + 1
            new_children = User(user_id=index, user_name=request.POST.get('signup_name'), user_age=int(request.POST.get('signup_age')),
                            user_sex=int(request.POST.get('gender')), user_class=int(request.POST.get('signup_class')), parents_id=request.POST.get('signup_uid'))
            new_user.save()
            new_children.save()

            startarray = [datetime.time(9, 0, 0), datetime.time(10, 0, 0), datetime.time(11, 0, 0),
                        datetime.time(12, 0, 0), datetime.time(
                            13, 0, 0), datetime.time(14, 0, 0),
                        datetime.time(15, 0, 0)]
            endarray = [datetime.time(9, 50, 0), datetime.time(10, 50, 0), datetime.time(11, 50, 0),
            datetime.time(12, 50, 0), datetime.time(
                13, 50, 0), datetime.time(14, 50, 0),
            datetime.time(15, 50, 0)]

            for j in range(7):
                for i in range(1, 6):
                    savetimetable = Timetable()
                    savetimetable.subject_day = i
                    savetimetable.user_id = index
                    savetimetable.subject = ''
                    savetimetable.subject_start_time = startarray[j]
                    savetimetable.subject_finish_time = endarray[j]

                    savetimetable.save()

            return redirect('/')
            
    else:
        return render(request, 'user/signup.html')


@csrf_exempt
def timetable(request):
    parent_id=request.session['uid']
    children = User.objects.filter(parents_id=parent_id).first()
    request.session['user_id'] = children.user_id
    request.session['user_name'] = children.user_name

    user_timetable = Timetable.objects.filter(user_id=children.user_id).order_by('subject_day','subject_start_time')
    mon = []
    tue = []
    wed = []
    thu = []
    fri = []

    for idx, i in enumerate(user_timetable):
        if idx <7 :
            mon.append(i.subject)
        elif idx < 14 :
            tue.append(i.subject)
        elif idx < 21 :
            wed.append(i.subject)
        elif idx < 28 :
            thu.append(i.subject)
        else :
            fri.append(i.subject)


    
    content = {'mon' : mon, 'tue' : tue, 'wed':wed, 'thu':thu, 'fri':fri}

    return render(request, "user/timetable.html", content)


@csrf_exempt
def timetablevalue(request):
    print("ajax success")
    if request.method == "POST":
        data = request.POST.get('id')
        data = data[1:-1].replace('"', '').split(',')
        parent_id=request.session['uid']
        children = User.objects.filter(parents_id=parent_id).first()
        # print(data)
        # print(f"data : {data}" )
        # print(f"data type : {type(data)}")
        user_timetable = Timetable.objects.filter(user_id=children.user_id).order_by('subject_day','subject_start_time')
        for idx,i in enumerate(user_timetable):
            i.subject = data[idx]
            i.save()  

    return HttpResponse('')
    

@csrf_exempt
def profile(request):
    parents_id=request.session.get('parents_id')

    if request.method=="POST":
        if request.POST.get('user_id') and request.POST.get('user_name') and request.POST.get('user_age') and request.POST.get('user_sex') and request.POST.get('user_class') and request.POST.get('grade'):
            saverecord=User()
            saverecord.user_id=request.POST.get('user_id')
            saverecord.user_name=request.POST.get('user_name')
            saverecord.user_age=request.POST.get('user_age')
            saverecord.user_sex=request.POST.get('user_sex')
            saverecord.user_class=request.POST.get('user_class')
            saverecord.grade=request.POST.get('grade')
            saverecord.parents_id=request.session.get('parents_id')

            saverecord.save()

            messages.success(request, "프로필 수정 완료")
            request.session['user_name']=request.POST.get('user_name')
            return render(request, 'user/profile.html', {})

            # return redirect("/app/report")
    else:
        return render(request, 'user/profile.html', {'parents':parents_id})
        # return redirect("/app/report")

def mypage(request):

    if request.method == "POST":
        pass
    else:
        content = {}
        
        children = User.objects.filter(parents_id=request.session['uid'])

        for data in children:
            content[data.user_id] = [data.user_name, data.user_age]

        return JsonResponse(content)

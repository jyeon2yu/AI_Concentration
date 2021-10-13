from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from mysql import DB
from django.contrib import messages
from app.models import Parents, User
from django.views.decorators.csrf import csrf_exempt

from django.core.exceptions import ObjectDoesNotExist

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
            return redirect('/')
            
    else:
        return render(request, 'user/signup.html')

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

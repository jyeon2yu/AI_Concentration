from django.shortcuts import render
from django.http import HttpResponse
<<<<<<< HEAD
# from mysql import DB
=======
from mysql import DB
>>>>>>> 726f0271272c9461293c8ee88f8f0e7bdc242bec


# Create your views here.

def login(request):
    return HttpResponse('Hello, login!')

def db_check(request):
<<<<<<< HEAD
    # database = DB()
    # database.db_create()
=======
    database = DB()
    database.db_create()
>>>>>>> 726f0271272c9461293c8ee88f8f0e7bdc242bec
    print('db 생성 완료')
    return HttpResponse('DB 생성 page')

def db_insert(request):
    pass

def db_select(request):
    pass
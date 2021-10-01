from django.shortcuts import render
from django.http import HttpResponse
from mysql import DB


# Create your views here.

def login(request):
    return HttpResponse('Hello, login!')

def db_check(request):
    database = DB()
    database.db_create()
    print('db 생성 완료')
    return HttpResponse('DB 생성 page')

def db_insert(request):
    pass

def db_select(request):
    pass
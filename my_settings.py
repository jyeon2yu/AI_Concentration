# import mysql

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aiconcd',
        'USER': 'root',
        'PASSWORD': '123456', # 본인 비밀번호 넣기
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
SECRET_KEY = '' # 본인 프로젝트 시크릿키 넣기
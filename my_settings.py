import mysql

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aiconcd',
        'USER': 'root',
        'PASSWORD': '', # 본인 비밀번호 넣기
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

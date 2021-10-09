# import mysql

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aiconcd',
        'USER': 'root',
        'PASSWORD': '1234qwer', # 본인 비밀번호 넣기
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
SECRET_KEY = 'django-insecure-l+6zt=h9z$84q&jj%bhpss+t6=l(v0qa5z(gh4*)q_2710t2b#'

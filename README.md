# AI_Concentration
딥러닝을 활용한 우리AI 집중도 검사 프로그램의 Web report<br>

아래 순서대로 환경설정을 진행한 후, 각 폴더에 맞게 깃허브에서 다운받은 파일을 추가해 주면된다.<br>
단, my_settings.py 파일의 경우 주석으로 표시된 곳에 본인의 MySQL 비밀번호를 입력해준다.

<h3>1. 장고 가상환경 만들기</h3>
<b>python -m venv mysite</b> <br>
[참고]<br>
https://jyeon2yu.tistory.com/5?category=952587

<h3>2. 장고 설치하기</h3>
<b>python -m pip install --upgrade pip <br>
pip install django</b>

<h3>3. 장고 프로젝트 생성하기</h3>
<b>django-admin startproject config . </b><br>

<h3>4. 파이썬 패키지 설치하기</h3>
[참고]<br>
https://jyeon2yu.tistory.com/25?category=965625

<h3>5. 장고 앱 설치하기</h3>
<b>django-admin startapp app <br>
django-admin startapp user</b>

<h3>6. 장고와 MySQL 연동하기</h3>
[참고] <br>
https://jyeon2yu.tistory.com/39?category=952587

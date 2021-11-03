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

# AI_Concentration Description
![image](https://user-images.githubusercontent.com/45540117/140092656-d896666a-ae94-4282-8a4b-6d157d99d4b9.png)

<h3>Tools</h3>

![image](https://user-images.githubusercontent.com/45540117/140093012-ce0bb3ce-7ab7-4c0d-97be-e9bf0ecbbe79.png)


<h3>Architecture</h3>

![image](https://user-images.githubusercontent.com/45540117/140093160-1446819c-4a74-4560-bbdc-4ea84cfcef9d.png)


<h3>Deep Learning models</h3>
📌 <b>No deep learning code included in this project!</b><br>
We store the result of the deep learning model in the database, then fetch the data and visualize it on the web.

1. SSD
2. Conbolution Neural Networks(CNN)
3. Residual Masking Network

<h3>Web design</h3>

![image](https://user-images.githubusercontent.com/45540117/140094249-cac5e3a9-3352-4de5-848b-aa437a7a7473.png)

 

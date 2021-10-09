use aiconcd;

insert into images values
('emo_0','/static/img/emo_0.png'),
('emo_1','/static/img/emo_1.png'),
('emo_2','/static/img/emo_2.png'),
('emo_3','/static/img/emo_3.png'),
('emo_4','/static/img/emo_4.png'),
('emo_5','/static/img/emo_5.png'),
('emo_6','/static/img/emo_6.png'),
('grade_1','/static/img/grade_1.png'),
('grade_2','/static/img/grade_2.png'),
('grade_3','/static/img/grade_3.png'),
('grade_4','/static/img/grade_4.png'),
('grade_5','/static/img/grade_5.png');

insert into images values ('emo_00','C:/dev/python/AI_Conc/static/img/emo_00.png');
delete from images where image_name = 'emo_00';
drop table images;

update images set url="C:/dev/python/AI_Conc/static/img/emo_0.png" where image_name='emo_0';
update images set url="C:/dev/python/AI_Conc/static/img/emo_1.png" where image_name='emo_1';
update images set url="C:/dev/python/AI_Conc/static/img/emo_2.png" where image_name='emo_2';
update images set url="C:/dev/python/AI_Conc/static/img/emo_3.png" where image_name='emo_3';
update images set url="C:/dev/python/AI_Conc/static/img/emo_4.png" where image_name='emo_4';
update images set url="C:/dev/python/AI_Conc/static/img/emo_5.png" where image_name='emo_5';

update images set url="C:/dev/python/AI_Conc/static/img/grade_1.png" where image_name='grade_1';
update images set url="C:/dev/python/AI_Conc/static/img/grade_2.png" where image_name='grade_2';
update images set url="C:/dev/python/AI_Conc/static/img/grade_3.png" where image_name='grade_3';
update images set url="C:/dev/python/AI_Conc/static/img/grade_4.png" where image_name='grade_4';
update images set url="C:/dev/python/AI_Conc/static/img/grade_5.png" where image_name='grade_5';
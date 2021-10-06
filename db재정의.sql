show databases;
use aiconcd;
create user 'ai'@'%' identified by '1234';
grant all privileges on aiconcd.* to 'ai'@'%';
flush privileges;

use mysql;
select user, host from user;
show variables like 'PORT';

drop database aiconcd;
create database aiconcd;
use aiconcd;

drop table user;
CREATE TABLE IF NOT EXISTS `User` ( 
        `user_id` varchar(100) PRIMARY KEY NOT NULL,    
        `user_name` VARCHAR(50) NOT NULL,
        `user_age` TINYINT NOT NULL,
        `user_sex` boolean NOT NULL,
        `user_class` INT NOT NULL, 
        `grade` TINYINT,
        `parents_id` varchar(100)
        );
        
CREATE TABLE IF NOT EXISTS `Frame` ( 
        `user_id` varchar(100) NOT NULL,    
        `filename` CHAR(25) NOT NULL,
        `emotion` TINYINT NOT NULL,
        `emotion_prob` FLOAT NOT NULL,
        `is_eyeopen` TINYINT NOT NULL, 
        `is_seat` TINYINT NOT NULL,
        PRIMARY KEY (user_id, filename),
        FOREIGN KEY (user_id) REFERENCES `User` (user_id)
        );



drop table timetable;
CREATE TABLE IF NOT EXISTS `Timetable` (  
		`class` INT NOT NULL,
        `subject` VARCHAR(100) NOT NULL, 
        `subject_day` TINYINT NOT NULL,
        `subject_start_time` TIME NOT NULL,
        `subject_finish_time` TIME NOT NULL,
        `user_id` varchar(100) NOT NULL,
        PRIMARY KEY (class, subject, subject_day, user_id),
        UNIQUE KEY uk_name (subject_day, subject_start_time, subject_finish_time),
        FOREIGN KEY (`user_id`) REFERENCES `User` (`user_id`)
        );

drop table User_Conc;
CREATE TABLE  IF NOT EXISTS `User_Conc` ( 
        `user_id` varchar(100) NOT NULL,   
        `day_conc` DATE NOT NULL,
        `subject` VARCHAR(100) NOT NULL,
        `total_subject_time_conc` INT NOT NULL,
        `eye_close_time` INT NOT NULL,
        `not_seat_time` INT NOT NULL,
        `total_conc_time` INT NOT NULL,
        PRIMARY KEY (user_id, day_conc, `subject`),
        FOREIGN KEY (user_id) REFERENCES `User` (user_id)
        );

drop table user_emotion;
CREATE TABLE IF NOT EXISTS `User_Emotion` ( 
        `user_id` varchar(100) NOT NULL,   
        `day_emo` DATE NOT NULL,
        `subject` VARCHAR(100) NOT NULL,
        `sub_emotion` INT NOT NULL,
        `sub_emotion_time` INT NOT NULL,
        PRIMARY KEY (user_id, day_emo, subject, sub_emotion),
        FOREIGN KEY (user_id) REFERENCES `User` (user_id)
        );
        
CREATE TABLE IF NOT EXISTS `Parents` ( 
        `parents_id` VARCHAR(100) PRIMARY KEY,   
        `parents_pw` VARCHAR(100)
        );
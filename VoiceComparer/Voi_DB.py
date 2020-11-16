import mysql.connector
import librosa

import base64

db = mysql.connector.connect(host = 'localhost' , user = 'root' , passwd = 'root')

my = db.cursor()

#my.execute('create database Voice_Comparer')

#my.execute('show databases')

my.execute('use Voice_Comparer')
try :
    my.execute('create table Student (StudentID BIGINT NOT NULL , name varchar(30) , Branch varchar(10) ,class varchar(7) , sec char(1) , Year varchar(15) , PRIMARY KEY (StudentID) )')
except Exception as e:
    print('already Created')

try:
    my.execute('create table Student_Data_By_Path (StudentID BIGINT NOT NULL , File varchar(2000) , Label varchar(20) , FOREIGN KEY (StudentID) references Student(StudentID))')
    print('created')
except Exception as e:
    print('already Created')





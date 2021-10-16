#*****************Sports Club Management System*******************
import mysql.connector,time
_host='localhost'
_user='root'
_password=''
try:
    db=mysql.connector.connect(host=_host,user=_user,password=_password)
    if db.is_connected():
        cursor=db.cursor()
        cursor.execute('create database scms')
        cursor.execute('use scms')
        member_string='create table member( memberCode int(5) primary key,\
        memberName varchar(25),dateOfJoining date,address varchar(50),phoneNumber bigint(11),\
        facilityCode1 int(5),facilityCode2 int(5),facilityCode3 int(5),children int(2))'
        fees_string='create table fees( memberCode int(5), dateOfSubmission date,\
        amount decimal(10,2),primary key (memberCode, dateOfSubmission),\
        constraint fk_memCode foreign key (memberCode) references member(memberCode))'
        facility_string='create table facility( facilityCode int(5) primary key, facility varchar(20))'
        cursor.execute(member_string)
        cursor.execute(fees_string)
        cursor.execute(facility_string)

        print('>>> System Successfully Installed !')
    else:
        print('>>> Database Connection Failed. Retry !')
        time.sleep(1)
        exit()
except:
    print('>>> Internal Server Error Occurred !')
    time.sleep(1)
    exit()

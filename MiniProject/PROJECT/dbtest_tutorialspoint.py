import os
import time
import datetime
import MySQLdb
import mysql.connector
global c
#import mysql.connector
#from mysql.connector import Error
global db
import random

def getCPUtemperature():
    t_cpu = random.randint(12,18)
    return(t_cpu)


zeit = (datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"))
datum = (datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d"))
temperatur=getCPUtemperature()
print (str(temperatur)+ " - " + str(zeit) + " - " + str(datum))
db = mysql.connector.connect(host="192.168.43.93",user="ranga",passwd="hpranga44",database="main_table")
sql =  "INSERT INTO master_table (ENTRY, ROLLNUM,NAME,SUBJECTCODE,ATTENDANCE, DATE) VALUES (%s, %d, %s, %s, %s, %s)"
c= db.cursor()
c.execute(sql,( str(zeit) , temperatur,str("xyz"),str("19EC61"), str("P"),str(datum)))
db.commit()
print("write successfull")
'''
except mysql.connector.Error as error:
    print("failure")
    db.rollback()
'''

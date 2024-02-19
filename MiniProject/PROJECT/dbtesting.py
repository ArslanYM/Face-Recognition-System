import os
import time
import datetime
import MySQLdb
global c

global db
import random

def getCPUtemperature():
    t_cpu = random.randint(12,18)
    return(t_cpu)

def insert_to_db():
    temperatur = (getCPUtemperature())
    zeit = (datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"))
    datum = (datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d"))
    print (str(temperatur)+ " - " + str(zeit) + " - " + str(datum))
    sql =  "INSERT INTO master_table (ENTRY, ROLLNUM,NAME,SUBJECTCODE,ATTENDANCE, DATE) VALUES (%s, %d, %s, %s, %s, %s)" 
    try:
        c.execute(sql,( str(zeit) , temperatur,str("xyz"),str("19EC61"), str("P"),str(datum)))
        db.commit()
    except:
        rollback()
        #db.close()
'''
def read_from_db():
    try:
        #c.execute("SELECT * FROM TAB_CPU WHERE ID = (SELCET MAX(ID) FROM TAB_CPU)")
        c.execute("SELECT * FROM TAB_CPU ORDER BY ID DESC LIMIT 1")      
        result = c.fetchall()
        if result is not None:
             print ('CPU temperature: ' , result[0][1], '| time: ' , result[0][3], ' | datum: ' , result[0][2])
    except:
        print ("read error")
'''
def main():
    while 1:
        insert_to_db()
        #read_from_db()
        time.sleep(10)

if __name__ == '__main__':
    try:
        db = MySQLdb.connect("localhost","root","hpranga44","main_table")
        c= db.cursor()
    except:
        print ("Keine Verbindung zum Server...")
             
    try:
      main()
    except KeyboardInterrupt:
      print ("bye bye...")
      pass    
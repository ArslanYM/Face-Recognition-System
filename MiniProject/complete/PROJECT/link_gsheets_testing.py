import datetime
import psutil
import requests

data_to_send={}

data_to_send["Date"]=str(datetime.datetime.now())
data_to_send["Roll number"]=str('1904109')
data_to_send["Subject"]=str('Ml')
data_to_send["Attendance"]=str('A')

print(data_to_send)

r=requests.post("https://hook.eu1.make.com/g9kjc2g965zrruqf7e15oz65rkpjuoiz",json=data_to_send)
print(r.status_code)
import datetime
import math
#now=datetime.datetime.now()
time = datetime.datetime

print(time.now())
#print(now)

#print(time.now().time().isoformat(timespec='minutes'))
#print(time.now().date())

#time = datetime.datetime.fromisoformat(str)
#print(time.time().isoformat(timespec='seconds'))
#print(now.date().strftime("%d-%m-%y"))

strt = '2022-07-28 13:57:47.624667'#print(now.date())
'''
diference = time1 - time2
print(time1)
print(time2)
print(diference.seconds/60)
'''
datetime_start= datetime.datetime.fromisoformat(strt)
datetime_end= time.now()

minutes_diff = (datetime_end - datetime_start).total_seconds() / 60.0
parte_decimal, parte_entera = math.modf(minutes_diff)
print(str(int(parte_entera)),':',str(int(parte_decimal*60)).rjust(2, '0'))

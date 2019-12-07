import face_recognize as fr
import numpy as np

Date = fr.getdate()
fil = open("Log.txt","r")
data = []
for owrd in fil.read().split():
	data.append(owrd)
if data[0] == "DD|MM|YYYY":
	data = data[1:]
print(data)
fil.close()
f = open(fr.sequencefile,"r+")
a = [Date]
for line in f.read().split():
	a.append(line)
print(a)
fil = open("log.txt","a+")
fil.write("\n"+ Date+"\t")
for no in data:
	if no in a:
		fil.write("Present   ")
	else:
		fil.write("Absent    ")
fil.close()


fil = open("log.txt","r")
beta = []
no_of_days,size = 0,0
for line in fil:
	for word in line.split():
		if word == 'Present' :
			beta.append(1)
		elif word =="Absent":
			beta.append(0)
		else:
			beta.append(word)
		size+=1
	no_of_days+=1

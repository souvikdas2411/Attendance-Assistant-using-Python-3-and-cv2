import os
import sys
from datetime import datetime

import cv2
import numpy

import create_data as cd


def getdate():
	date = datetime.now()
	ans = str(date.day)+"|"+str(date.month)+"|"+str(date.year)
	return ans

array_to_store_names=[]

print('INITIALISING') 

(images, lables, names, id) = ([], [], {}, 0) 
for (subdirs, dirs, files) in os.walk(cd.datasets): 
	for subdir in dirs: 
		names[id] = subdir 
		subjectpath = os.path.join(cd.datasets, subdir) 
		for filename in os.listdir(subjectpath): 
			path = subjectpath + '/' + filename 
			lable = id
			images.append(cv2.imread(path, 0)) 
			lables.append(int(lable)) 
		id += 1
(width, height) = (130, 100) 

(images, lables) = [numpy.array(lis) for lis in [images, lables]] 


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(images, lables) 

face_cascade = cv2.CascadeClassifier(cd.haar_file) 
webcam = cv2.VideoCapture(0) # ----- webcam
#cap = cv2.VideoCapture('http://192.168.43.7:8080/video') #----- mobile_streaming

sequencefile=getdate()
print(sequencefile)
sequencefile+=".txt"
while True: 
	(_, im) = webcam.read()
	#(_, im) = cap.read() 
	gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
	faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
	for (x, y, w, h) in faces: 

		cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2) 
		face = gray[y:y + h, x:x + w] 
		face_resize = cv2.resize(face, (width, height)) 
		prediction = recognizer.predict(face_resize) 
		cv2.rectangle(im, (x, y), (x + w, y + h), (255, 255, 0), 3)

		if names[prediction[0]] not in array_to_store_names:
			cv2.rectangle(im, (x, y), (x + w, y + h), (255, 255, 0), 3) 
			cv2.putText(im, '% s' %(names[prediction[0]]), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 
			print("REGISTERED %s"%(names[prediction[0]]))
			array_to_store_names.append(names[prediction[0]])
			f=open(sequencefile,"a+")
			f.write("%s" %(names[prediction[0]])+ "\n")

	cv2.imshow('OpenCV', im) 
	if cv2.waitKey(1) & 0xFF==ord('q'): 
		f.close()
		break

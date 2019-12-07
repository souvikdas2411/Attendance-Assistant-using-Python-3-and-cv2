import cv2, sys, numpy, os 
haar_file = 'cascade.xml'
datasets = 'datasets'


if __name__ == "__main__":
	

	(width, height) = (130, 100)	 

	face_cascade = cv2.CascadeClassifier(haar_file) 
	webcam = cv2.VideoCapture(0) #1 for any other cam
	# cam = cv2.VideoCapture('http://192.168.43.7:8080/video')
	f = open("Log.txt","a+")
	f.seek(0)
	chk = f.read(1)
	if not chk:
		f.write("DD|MM|YYYY\t")
	else:
		f.seek(0,2) # 2 is to the eof
	sub_data = input("Enter Name : ")	
	if sub_data == 'q':
		exit()
	path = os.path.join(datasets, sub_data) 
	if not os.path.isdir(path): 
		os.mkdir(path) 
	count = 0
	while count >= 0: 
		(_, im) = webcam.read() 
		gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
		faces = face_cascade.detectMultiScale(gray, 1.3, 4) 
		for (x, y, w, h) in faces: 
			cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2) 
			face = gray[y:y + h, x:x + w] 
			face_resize = cv2.resize(face, (width, height)) 
			cv2.imwrite('% s/% s.png' % (path, count), face_resize) 
		count += 1
		cv2.imshow('OpenCV', im)  
		if cv2.waitKey(1) & 0xFF==ord('q'):
			break
	f.write(sub_data+"\t")
    # f.close()
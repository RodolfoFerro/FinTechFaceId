import numpy as np
import cv2, requests

def distancia(p1,p2):
	X = p1[0] - p2[0]
	Y = p1[1] - p2[1]
	return np.sqrt(X**2+Y**2)

def face_capture():
	# Load Data:
	cascPath = "haarcascades/"
	face_cascade = cv2.CascadeClassifier(cascPath+'haarcascade_frontalface_default.xml')
	nose_cascade = cv2.CascadeClassifier(cascPath+'haarcascade_mcs_nose.xml')

	# Open Webcam
	cap = cv2.VideoCapture(0)

	while True:
		ret, img = cap.read()
		# Gray scaling
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# Find face sing Haar Cascades
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		if len(faces):
			for (x,y,w,h) in faces[:1]:
				#cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
				# Draw an ellipse
				cv2.ellipse(img,(x+w/2,y+h/2),(h/2,w/2+w/10),0,0,360,(255,0,0),2)
				roi_gray = gray[y:y+h, x:x+w]
				roi_color = img[y:y+h, x:x+w]
				
				nose = nose_cascade.detectMultiScale(roi_gray)
				for (ex,ey,ew,eh) in nose[:1]:
					#cv2.circle(roi_color,(ex+ew/2,ey+eh/2),(ew+eh)/8,(0, 255, 0), 2)
					#cv2.ellipse(roi_color,(ex+ew/2,ey-eh/6),(eh/2,ew/2+ew/6),0,0,360,(0,255,0),2)
					cv2.line(roi_color,(ex+ew/2,ey-eh/6-ew/2-ew/6),(ex+ew/2,ey-eh/6+ew/2+ew/6),(0,0,255),2)
					cv2.circle(roi_color,(ex+ew/2,ey-eh/6-ew/2-ew/6),2,(0,255,0),2)
					cv2.circle(roi_color,(ex+ew/2,ey-eh/6+ew/2+ew/6),2,(0,255,0),2)
					#cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
			# Show image:
			cv2.imshow('Face Detection',img)
			k = cv2.waitKey(30) & 0xff
			if k == 32:
				# Save image
				cv2.imwrite("snap.jpg", img)
				break

	cap.release()
	cv2.destroyAllWindows()
	return [[ex+ew/2,ey-eh/6-ew/2-ew/6],[ex+ew/2,ey-eh/6+ew/2+ew/6]]

def relevant_points_eyes(name):
	# Load Data:
	cascPath = "haarcascades/"
	eye_cascade = cv2.CascadeClassifier(cascPath+'haarcascade_mcs_eyepair_big.xml')

	img = cv2.imread(name)
	eyes = eye_cascade.detectMultiScale(img)
	for (ex,ey,ew,eh) in eyes[:1]:
		#cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
		cv2.circle(img,(ex+ew/5,ey+eh/2),(ew+eh)/8,(0,0,255),2)
		cv2.circle(img,(ex+ew-ew/5,ey+eh/2),(ew+eh)/8,(0,0,255),2)
		cv2.circle(img,(ex+ew/5,ey+eh/2),2,(0,255,0),2)
		cv2.circle(img,(ex+ew-ew/5,ey+eh/2),2,(0,255,0),2)
	cv2.imshow('Relevant Points',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return [[ex+ew/5,ey+eh/2], [ex+ew-ew/5,ey+eh/2]]

def main():
	rel_points = []
	rel_points.append(face_capture())
	rel_points.append(relevant_points_eyes("snap.jpg"))
	num = distancia(rel_points[0][0],rel_points[0][1])
	den = distancia(rel_points[1][0],rel_points[1][1])
	factor = num / float(den)
	requests.post("http://localhost:8000/fact", data={"factor":factor})

if __name__ == "__main__":
	print "Yeah!"
	main()
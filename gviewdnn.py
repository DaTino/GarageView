import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.1,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

CLASSES = ["person"]

#CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
#	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
#	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
#	"sofa", "train", "tvmonitor"]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))


print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()

numobj = 0

while True:

	frame = vs.read()
	frame = imutils.resize(frame, width=1000)

	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
		0.007843, (300, 300), 127.5)

	net.setInput(blob)
	detections = net.forward()
	
	cv2.line(frame, (470, 0), (470, 560), (0,255,0), 5)
	cv2.line(frame, (530, 0), (530, 560), (0,255,0), 5)
	

	for i in np.arange(0, detections.shape[2]):

		confidence = detections[0, 0, i, 2]

		if confidence > args["confidence"]:
			
			idx = int(detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			#label = "{}: {:.2f}%".format(CLASSES[idx],
			#	confidence * 100)
			#Use this to choose what you wanna search for
			#if (CLASSES[idx] == "bottle"):
			#cv2.rectangle(frame, (startX, startY), (endX, endY),
			#	COLORS[idx], 2)
			#y = startY - 15 if startY - 15 > 15 else startY + 15
			#cv2.putText(frame, label, (startX, y),
			#	cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
				#if (((startX+endX)/2) >=470 and ((startX+endX)/2 <= 530)):
					#numobj+=1
			
		
			label = "{}: {:.2f}%".format(CLASSES[0], confidence * 100)
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLORS[0], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			cv2.putText(frame, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[0], 2)
			if (((startX+endX)/2) >=470 and ((startX+endX)/2 <= 530)):
				numobj+=1




	
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

	fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
print(numobj)

cv2.destroyAllWindows()
vs.stop()

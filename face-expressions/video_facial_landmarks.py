# tutorial from https://www.pyimagesearch.com/2017/04/17/real-time-facial-landmark-detection-opencv-python-dlib/

# USAGE - you NEED a shape predictor with this. hopefully it's included with the file.
# python video_facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat
# python video_facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat --picamera 1

# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import datetime
import argparse
import imutils
import time
import dlib
import cv2
import numpy as np
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-r", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
 
# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(0.5)

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream, resize it to
	# have a maximum width of 400 pixels, and convert it to
	# grayscale
	frame = vs.read()
	frame = imutils.resize(frame, width=800)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces in the grayscale frame
	rects = detector(gray, 0)




	# loop over the face detections
	for id_, rect in enumerate(rects):
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array

		# Draw rectangle around the face
		rect_left_top = (rect.left(), rect.top())
		rect_right_bottom = (rect.right(), rect.bottom())
		cv2.rectangle(frame, rect_left_top, rect_right_bottom, (255,0,0), 2)

		# print("left, top", rect_left_top, "\t", "right, bottom", rect_right_bottom)


		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)


		# print(shape[67])
		# print(type(shape))

		# Indexing is shifted by one!

		# Get useful landmarks
		top_lip = shape[62]
		bottom_lip = shape[66]
		left_lip = shape[48]
		right_lip = shape[54]

		# Compute distances of interest
		# rectangle diagonal
		rect_diag = np.linalg.norm(np.array(rect_left_top) - np.array(rect_right_bottom))
		# top and bottom lip
		lips_ver_dist = np.linalg.norm(top_lip - bottom_lip)
		# left and right lip
		lips_hor_dist = np.linalg.norm(left_lip - right_lip)

		# print(rect_diag)
		# print(lips_ver_dist)
		# print(lips_hor_dist)


		print("Person:", id_)

		# Detect smiling
		if (lips_hor_dist / rect_diag) > 0.27:
			print("Smiling")

		# Detect opened mouth
		if (lips_ver_dist / lips_hor_dist) > 0.2:
			print("Opened mouth")

		print()

		# loop over the (x, y)-coordinates for the facial landmarks
		# and draw them on the image
		for (x, y) in shape:
			cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
	  
	# show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
 
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
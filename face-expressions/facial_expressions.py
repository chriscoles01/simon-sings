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

import threading
import time
import multiprocessing as mp



class myThread(threading.Thread):

	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.q = mp.Queue()
		self.stop = False


	def run(self):
		print("Starting " + self.name)
		self.run_facial_expression_recognition(self.name)
		print("Exiting + " + self.name)

	def stop_thread(self):
		self.stop = True


	def run_facial_expression_recognition(self, threadName):

		# initialize dlib's face detector (HOG-based) and then create
		# the facial landmark predictor
		print("[INFO] loading facial landmark predictor...")
		detector = dlib.get_frontal_face_detector()
		predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

		# initialize the video stream and start the camera
		print("[INFO] camera starting up...")
		vs = VideoStream(0).start()

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

				colour = (0,0,0)

				if id_ == 0:
					colour = (255,0,0)
				elif id_ == 1:
					colour = (0,255,0)
				elif id_ == 2:
					colour = (0,0,255)

				cv2.rectangle(frame, rect_left_top, rect_right_bottom, colour, 2)

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
				eyebrow_left_inner = shape[21]
				eyebrow_right_inner = shape[22]

				# Compute distances of interest
				# rectangle diagonal
				rect_diag = np.linalg.norm(np.array(rect_left_top) - np.array(rect_right_bottom))
				# top and bottom lip
				lips_ver_dist = np.linalg.norm(top_lip - bottom_lip)
				# left and right lip
				lips_hor_dist = np.linalg.norm(left_lip - right_lip)
				# inner edges of eyebrows
				eyebrow_inner_dist = np.linalg.norm(eyebrow_left_inner - eyebrow_right_inner)

				# print(rect_diag)
				# print(lips_ver_dist)
				# print(lips_hor_dist)


				print("Person:", id_)

				# Detect smiling
				if (lips_hor_dist / rect_diag) > 0.3:
					print("Smiling")

				# Detect opened mouth
				if (lips_ver_dist / lips_hor_dist) > 0.2:
					print("Opened mouth")

				# Detect frowning
				# if (eyebrow_inner_dist / rect_diag) < 0.08:
				if (eyebrow_inner_dist / rect_diag) < 0.1:

					print("Frowning")

				print()

				# loop over the (x, y)-coordinates for the facial landmarks
				# and draw them on the image
				for (x, y) in shape:
					cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

				if self.stop:
					raise Exception("You've just wished to kill the thread. So did I.")


			# show the frame
			# cv2.imshow("Frame", frame)
			self.q.put(frame)

			# sleep
			time.sleep(0.1)
		
		# do a bit of cleanup
		cv2.destroyAllWindows()
		vs.stop()

if __name__ == '__main__':
	# Create new threads
	thread1 = myThread(1, "Facial-Thread")
	# Start new Threads
	thread1.start()
	while True:
		frame = thread1.q.get()
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			thread1.stop_thread()
			break

	print ("Exiting Main Thread")
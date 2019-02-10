# adapted from https://www.pyimagesearch.com/2017/04/17/real-time-facial-landmark-detection-opencv-python-dlib/

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

class FacialExpressionDetector(threading.Thread):

	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.q = mp.Queue()
		self.stop = False
		# dictionary to store players expressions under their id, None stands for no expressions
		self.expressions = {0: None, 1: None} 

	def get_expression(self, id_):
		while True:
			expression = self.expressions[id_]
			if expression is not None:
				return expression



	def run(self):
		print("Starting " + self.name)
		self.run_facial_expression_recognition(self.name)
		print("Exiting + " + self.name)

	
	def stop_thread(self):
		self.stop = True


	def draw_face(self, id_, rect, frame, shape):
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

		# loop over the (x, y)-coordinates for the facial landmarks
		# and draw them on the image
		for (x, y) in shape:
			cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)


	def process_face(self, id_, rect, shape):
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
		rect_diag = np.linalg.norm(np.array((rect.left(), rect.top())) - np.array((rect.right(), rect.bottom())))
		# top and bottom lip
		lips_ver_dist = np.linalg.norm(top_lip - bottom_lip)
		# left and right lip
		lips_hor_dist = np.linalg.norm(left_lip - right_lip)
		# inner edges of eyebrows
		eyebrow_inner_dist = np.linalg.norm(eyebrow_left_inner - eyebrow_right_inner)

		print("Person:", id_)

		# Detect smiling
		if (lips_hor_dist / rect_diag) > 0.3:
			self.expressions[id_] = 'smiling'
			print("Smiling")

		# Detect opened mouth
		elif (lips_ver_dist / lips_hor_dist) > 0.2:
			self.expressions[id_] = 'opened-mouth'
			print("Opened mouth")

		# Detect frowning
		elif (eyebrow_inner_dist / rect_diag) < 0.09:
			self.expressions[id_] = 'frowning'
			print("Frowning")
		
		# Otherwise None
		else:
			self.expressions[id_] = None

		print()


	def run_facial_expression_recognition(self, threadName):
		# initialize dlib's face detector (HOG-based) and then create
		# the facial landmark predictor
		print("[INFO] loading facial landmark predictor...")
		self.detector = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor('../lib/shape_predictor_68_face_landmarks.dat')

		# initialize the video stream and start the camera
		print("[INFO] camera starting up...")
		vs = VideoStream(0).start()

		# loop over the frames from the video stream
		while True:
			# grab the frame from the threaded video stream, resize it to
			# have a maximum width of 800 pixels, and convert it to
			# grayscale
			frame = vs.read()
			# print(frame)
			frame = imutils.resize(frame, width=800)
			gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			# detect faces in the grayscale frame
			rects = self.detector(gray_frame, 0)	# type dlib.rectanles
			rects_lst = list(rects)
			rects_lst.sort(key=lambda r: r.left())

			# loop over the face detections
			for id_, rect in enumerate(rects_lst):
				shape = self.predictor(gray_frame, rect)
				shape = face_utils.shape_to_np(shape)
				self.draw_face(id_, rect, frame, shape)
				self.process_face(id_, rect, shape)

				if self.stop:
					raise Exception("You've just wished to kill me. So I did a suicide.")

			# show the frame
			# cv2.imshow("Frame", frame)
			if self.q.full():
				print("Full queue")
				self.q.qet()

			self.q.put(frame)
			time.sleep(0.1)
		
		# do a bit of cleanup
		cv2.destroyAllWindows()
		vs.stop()


if __name__ == '__main__':
	# Create new threads
	thread1 = FacialExpressionDetector(1, "Facial-Thread")
	# Start new Threads
	thread1.start()

	counter = 0

	while True:
		frame = thread1.q.get()
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			thread1.stop_thread()
			break

		# counter += 1
		# if counter % 1 == 0:
		# 	print(thread1.get_expression(0))


	print ("Exiting Main Thread")
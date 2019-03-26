import cv2
from flask import Flask, Response
import dlib
import time
import datetime
import threading
from threading import Thread
from pathlib import Path

class FrameManager(object):
	def __init__(self):
		self.lock = threading.Lock()
		self.lock_save = threading.Lock()
		self.to_upload = []
		
		self.cam = cv2.VideoCapture(0)
		self.ret, self.frame = self.cam.read()
		
	def update(self):   
		self.lock.acquire()
		try:
			self.ret, self.frame = self.cam.read()
		finally:
			self.lock.release()
			
	def read(self):
		self.lock.acquire()
		frame = self.frame.copy()
		self.lock.release()
		return frame
	
	def __del__(self):
		self.cam.release()
		
	def append_list(self, filePath):
		self.lock_save.acquire()
		self.to_upload.append(filePath)
		self.lock_save.release()
	
	def pop_list(self):
		pop = None
		self.lock_save.acquire()
		if len(self.to_upload) > 0:
			pop = self.to_upload.pop(0)
		self.lock_save.release()    
		return pop
	
	def upload(self, sleepTime=1.0):
		while True:
			imgName = self.pop_list()
			if imgName:
				print('\r'+ str(len(self.to_upload)) + ' ' + imgName, end='', flush=True)
			time.sleep(sleepTime)
		
class FrameManagerWrapper(object):
	def __init__(self):
		self.fm = FrameManager()

	def uploadLoop(self):
		self.fm.upload()

	def readThread(self):
		while(True):
			self.fm.update()

class Vision(object):
	def __init__(self,fm=None):
		self.detector = dlib.get_frontal_face_detector()
		self.dets = None
		self.fm = fm
	def get_det_frame(self):
		image = self.fm.read()
		st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M_%S_%f')
		
		dets = self.detector(image, 1)
		for faceRect in dets:
			x1 = faceRect.left()
			y1 = faceRect.top()
			x2 = faceRect.right()
			y2 = faceRect.bottom()
			image = cv2.rectangle(image, (x1, y1), (x2, y2), (0,0,255))
		if len(dets) >= 2:
			st = 'log/'+st+'.jpg'
			cv2.imwrite(st, image)
			self.fm.append_list(st)
		
		ret, jpeg = cv2.imencode('.jpg', image)
		return jpeg.tobytes()

	def get(self):
		return self.dets

	def get_det_frame2(self):
		image = self.fm.read()
		st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M_%S_%f')
		
		dets = self.detector(image, 1)
		return len(dets)

class FlaskWrapper(object):
	def __init__(self):
		
		self.fmw = FrameManagerWrapper()
		self.vis = Vision(self.fmw.fm)
		self.app = Flask(__name__)
		self.app.add_url_rule('/', view_func=self.video_feed)
		self.app.add_url_rule('/warning', view_func=self.video_feed2)
		self.web_view = Thread(target=self.runApp,args=[])
		self.update_frame = Thread(target=self.fmw.readThread,args=[])
		self.upload_frame = Thread(target=self.fmw.uploadLoop,args=[])

	def gen(self):
		while True:
			frame = self.vis.get_det_frame()
			yield (b'--frame\r\n'
					b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
	
	def video_feed(self):
		return Response(self.gen(),
						mimetype='multipart/x-mixed-replace; boundary=frame')

	def video_feed2(self):
		frame, tam = self.vis.get_det_frame2()
		return str(tam)

	def runApp(self):
		self.app.run(host='0.0.0.0',port=5522)

	def runAll(self):
		self.update_frame.start()
		self.web_view.start()
		self.upload_frame.start()

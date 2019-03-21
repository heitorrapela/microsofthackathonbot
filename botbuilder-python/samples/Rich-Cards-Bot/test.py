import cv2
from flask import Flask, render_template, Response
import pdb
import numpy as np       
import dlib
import time
import datetime
import threading
from threading import Thread
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive
from pathlib import Path

class FrameManager(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.lock_save = threading.Lock()
        self.to_upload = []
        
        self.cam = cv2.VideoCapture(0)
        self.ret, self.frame = self.cam.read()
        
        #self.gauth = GoogleAuth()
        #self.gauth.LocalWebserverAuth()
        #self.drive = GoogleDrive(self.gauth)
        #self.fid = "1YvqVtqvseQk_swQ1Qj0BBI3g8mgfYQmb"
        
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
    
    def upload_file(self, filePath):
        pathImg = Path(filePath)
        imgName = pathImg.name
        f = self.drive.CreateFile({'title': imgName,
                              "parents": [{"kind": "drive#fileLink", "id": self.fid}]})
        f.SetContentFile(filePath)
        f.Upload()
    
    def upload(self, sleepTime=1.0):
        while True:
            imgName = self.pop_list()
            if imgName:
                print('\r'+ str(len(self.to_upload)) + ' ' + imgName, end='', flush=True)
                self.upload_file(imgName)
            time.sleep(sleepTime)
        
        
fm = FrameManager()

def uploadLoop():
    fm.upload()

def readThread():
    while(True):
        fm.update()

class Vision(object):
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()

    def get_det_frame(self):
        image = fm.read()
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M_%S_%f')
        
        dets = self.detector(image, 1)
        for faceRect in dets:
            x1 = faceRect.left()
            y1 = faceRect.top()
            x2 = faceRect.right()
            y2 = faceRect.bottom()
            image = cv2.rectangle(image, (x1, y1), (x2, y2), (0,0,255))
        if len(dets) > 0:
            st = 'log/'+st+'.jpg'
            cv2.imwrite(st, image)
            fm.append_list(st)
        
        ret, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes()

    def get_det_frame2(self):
        image = fm.read()
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M_%S_%f')
        
        dets = self.detector(image, 1)
        for faceRect in dets:
            x1 = faceRect.left()
            y1 = faceRect.top()
            x2 = faceRect.right()
            y2 = faceRect.bottom()
            image = cv2.rectangle(image, (x1, y1), (x2, y2), (0,0,255))
        if len(dets) != 1:
            st = 'log/'+st+'.jpg'
            cv2.imwrite(st, image)
            fm.append_list(st)
        
        ret, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes(), len(dets)

vis = Vision()


app = Flask(__name__)

def gen():
    while True:
        frame = vis.get_det_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen2():
    while True:
        frame, tam = vis.get_det_frame2()
        if(tam != 2):
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/warning')
def video_feed2():
    frame, tam = vis.get_det_frame2()
    return str(tam)


def runApp():
    app.run(host='0.0.0.0',port=5522)

web_view = Thread(target=runApp,args=[])
update_frame = Thread(target=readThread,args=[])
upload_frame = Thread(target=uploadLoop,args=[])

update_frame.start()
web_view.start()
upload_frame.start()
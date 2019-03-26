# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
This sample shows how to use different types of rich cards.
"""


from aiohttp import web
from pygame import mixer # Load the required library
import webbrowser

from botbuilder.schema import (Activity, ActivityTypes,
                               AnimationCard, AudioCard, Attachment,
                               ActionTypes, CardAction,
                               CardImage, HeroCard,
                               MediaUrl, ThumbnailUrl,
                               ThumbnailCard, VideoCard,
                               ReceiptCard, SigninCard,
                               Fact, ReceiptItem)
from botbuilder.core import (BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext,
                             ConversationState, MemoryStorage, UserState, CardFactory)
"""Import AdaptiveCard content from adjacent file"""
from adaptive_card_example import ADAPTIVE_CARD_CONTENT

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
                #self.upload_file(imgName)
            time.sleep(sleepTime)
        
        
fm = FrameManager()

def uploadLoop():
    fm.upload()

def readThread():
    while(True):
        fm.update()

teste = None

class Vision(object):
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.dets = None
    def get_det_frame(self):
        global teste
        image = fm.read()
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
            fm.append_list(st)
        
        ret, jpeg = cv2.imencode('.jpg', image)

        teste = dets
        return jpeg.tobytes()

    def get():
        return self.dets

    def get_det_frame2(self):
        image = fm.read()
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M_%S_%f')
        
        dets = self.detector(image, 1)
        return len(dets)

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


APP_ID = ''
APP_PASSWORD = ''
PORT = 9000
SETTINGS = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Create MemoryStorage, UserState and ConversationState
memory = MemoryStorage()
# Commented out user_state because it's not being used.
# user_state = UserState(memory)
conversation_state = ConversationState(memory)

# Register both State middleware on the adapter.
# Commented out user_state because it's not being used.
# ADAPTER.use(user_state)
ADAPTER.use(conversation_state)

import dlib

# Methods to generate cards
def create_baby_check_card() -> Attachment:
    global teste, vis
    
    ret = vis.get_det_frame2()
    if (ret < 1):
        msg = "Problem with baby"
    elif (ret > 1):
        msg = "More people wtih baby"
    else:
        msg = "Baby is ok"

    return msg


def create_check_env() -> Attachment:
    addr = "http://localhost:5522"
    webbrowser.open_new(addr)

def create_lullaby_play() -> Attachment:
    mixer.init()
    mixer.music.load('./song/song.mp3')
    mixer.music.play()

def create_lullaby_stop() -> Attachment:
    mixer.music.stop()

async def create_reply_activity(request_activity: Activity, text: str, attachment: Attachment = None) -> Activity:
    activity = Activity(
        type=ActivityTypes.message,
        channel_id=request_activity.channel_id,
        conversation=request_activity.conversation,
        recipient=request_activity.from_property,
        from_property=request_activity.recipient,
        text=text,
        service_url=request_activity.service_url)
    if attachment:
        activity.attachments = [attachment]
    return activity


async def handle_message(context: TurnContext) -> web.Response:
    # Access the state for the conversation between the user and the bot.
    state = await conversation_state.get(context)
    if hasattr(state, 'in_prompt'):
        if state.in_prompt:
            state.in_prompt = False
            return await card_response(context)
        else:
            state.in_prompt = True
            prompt_message = await create_reply_activity(context.activity, 'Hello, what do you want to do?\n'
                                                                           '(1) Check Image\n'
                                                                           '(2) Check Environment\n'
                                                                           '(3) Play Lullaby\n'
                                                                           '(4) Stop Lullaby\n'    )
            await context.send_activity(prompt_message)
            return web.Response(status=202)
    else:
        state.in_prompt = True
        prompt_message = await create_reply_activity(context.activity, 'Hello, what do you want to do?\n'
                                                                       '(1) Check Image\n'
                                                                       '(2) Check Environment\n'
                                                                       '(3) Play Lullaby\n'
                                                                       '(4) Stop Lullaby\n')
        await context.send_activity(prompt_message)
        return web.Response(status=202)


async def card_response(context: TurnContext) -> web.Response:
    response = context.activity.text.strip()
    choice_dict = {
        '1': [create_baby_check_card], 'Check Image': [create_baby_check_card],
        '2': [create_check_env], 'Monitor Environment': [create_check_env],
        '3': [create_lullaby_play], 'Play Lullaby': [create_lullaby_play],
        '4': [create_lullaby_stop], 'Stop Lullaby': [create_lullaby_play],
    }

    # Get the functions that will generate the card(s) for our response
    # If the stripped response from the user is not found in our choice_dict, default to None
    choice = choice_dict.get(response, None)
    # If the user's choice was not found, respond saying the bot didn't understand the user's response.
    if not choice:
        not_found = await create_reply_activity(context.activity, 'Sorry, I didn\'t understand that. :(')
        await context.send_activity(not_found)
        return web.Response(status=202)
    elif (response == '1'):
        msg = create_baby_check_card()
        response = await create_reply_activity(context.activity, msg)
        await context.send_activity(response)
    else:
        for func in choice:
            card = func()
            response = await create_reply_activity(context.activity, '', card)
            await context.send_activity(response)
        return web.Response(status=200)


async def handle_conversation_update(context: TurnContext) -> web.Response:
    if context.activity.members_added[0].id != context.activity.recipient.id:
        response = await create_reply_activity(context.activity, 'Welcome to the Super Nany Bot!')
        await context.send_activity(response)
    return web.Response(status=200)


async def unhandled_activity() -> web.Response:
    return web.Response(status=404)


async def request_handler(context: TurnContext) -> web.Response:
    if context.activity.type == 'message':
        return await handle_message(context)
    elif context.activity.type == 'conversationUpdate':
        return await handle_conversation_update(context)
    else:
        return await unhandled_activity()


async def messages(req: web.web_request) -> web.Response:
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers['Authorization'] if 'Authorization' in req.headers else ''
    try:
        return await ADAPTER.process_activity(activity, auth_header, request_handler)
    except Exception as e:
        raise e


app = web.Application()
app.router.add_post('/', messages)

try:
    web.run_app(app, host='localhost', port=PORT)
except Exception as e:
    raise e

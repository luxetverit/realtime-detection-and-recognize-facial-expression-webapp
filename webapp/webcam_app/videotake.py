import cv2
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
import numpy as np
from pathlib import Path
import json
from django.http import StreamingHttpResponse
import base64
from collections import Counter
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from .models import Counseling, DetectedEmotions
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from asgiref.sync import sync_to_async
import os





@database_sync_to_async
def get_counseling_object_or_404(pk):
    return get_object_or_404(Counseling, pk=pk)

@database_sync_to_async
def get_detectdedemotions_object_or_404(pk):
    return get_object_or_404(DetectedEmotions, pk=pk)

@database_sync_to_async
def set_detectdedemotions(detected_emotions,feelcount):
    if feelcount :
        print('onepiece')
        detected_emotions.anger=feelcount['anger']
        detected_emotions.anxiety=feelcount['anxiety']
        detected_emotions.embarrassed=feelcount['embarrassed']
        detected_emotions.hurt=feelcount['hurt']
        detected_emotions.neutral=feelcount['neutral']
        detected_emotions.pleasure=feelcount['pleasure']
        detected_emotions.sad=feelcount['sad']
        detected_emotions.save(update_fields=['anger','anxiety','embarrassed','hurt','neutral','pleasure','sad'])
    else: print('error')
   
        




BASE_DIR = Path(__file__).resolve().parent
CLASSES = ['anger','anxiety','embarrassed','hurt','neutral','pleasure','sad']
# 색상 랜덤하게 뽑아서 적용 다 다르게 
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))


def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = f'{CLASSES[class_id]} ({confidence:.2f})'
    color = colors[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    

# 모델 불러오기 
model = cv2.dnn.readNet(str(BASE_DIR)+"/best.onnx")


def cameracheck(video_capture) :
    if video_capture.isOpened():
        return True
    else: 
        return False


def cam_return():
        video_capture=cv2.VideoCapture(cv2.CAP_ANY,cv2.CAP_DSHOW)
        if cameracheck(video_capture) : #True False
            return video_capture
        
        
        else: 
            video_capture=cv2.VideoCapture(cv2.CAP_ANY,cv2.CAP_V4L2)
            return video_capture
   





# @csrf_exempt
class VideoConsumer(AsyncWebsocketConsumer):
        
        

    async def stop_streaming(self):
        self.stopped = True
        self.is_streaming = False
        self.video_capture.release()
        # self.out.release()
        # with open(f"media/cam/{self.counseling.pk}.mp4", 'rb') as f:
        #      await sync_to_async(self.counseling.storage_data.save)(f'{self.counseling.pk}.mp4', File(f))
        await sync_to_async(self.counseling.save)()
    
    async def connect(self):
        try:
            self.pk = self.scope['url_route']['kwargs']['counseling_id']
            self.feelcount=False
            self.task=''
            self.counseling = await get_counseling_object_or_404(self.pk)
            self.detected_emotions = await get_detectdedemotions_object_or_404(self.pk)
            await self.accept()
            self.video_capture = cam_return()
            self.camopen=cameracheck(self.video_capture)                                      
            self.frame_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)
            if self.fps==0:
                self.fps=10
            self.is_streaming = False
            self.filepath_to=str(BASE_DIR)+f'/{self.counseling.pk}.mp4'
            self.mediapaht=f"media/cam/{self.counseling.pk}.mp4"
            self.stopped = False
            # os.system('ls /dev/video*')
            # self.out=cv2.VideoWriter(self.mediapaht, fourcc, self.fps, (self.frame_width, self.frame_height))
        except Exception as e:    # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
            os.system('ls /dev/video*')
            print(f'예외가 발생했습니다. 카메라 이슈 :{self.camopen}', e)
            
    async def disconnect(self,close_code):
            self.is_streaming = False
            self.stopped = True
        
    
  
            
    async def stream_video(self):
        feelings=[]
        
        while self.is_streaming and not self.stopped  :
            ret, frame = self.video_capture.read()
            if not ret:
                break
            [height, width, _] = frame.shape
            length = max((height, width))
            image = np.zeros((length, length, 3), np.uint8)
            image[0:height, 0:width] = frame
            scale = length / 640
            
        #  Yolov8 모델은 전치해줘야 하나봄 
            blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(640, 640))
            model.setInput(blob)
            outputs = model.forward()
            outputs = np.array([cv2.transpose(outputs[0])])
            rows = outputs.shape[1]
            
            boxes = []
            scores = []
            class_ids = []
            
            
        # 한장의 사진에 각 x,y, confidence 받음 

            for i in range(rows):
                classes_scores = outputs[0][i][4:]
                (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
                if maxScore >= 0.25:
                    box = [
                        outputs[0][i][0] - (0.5 * outputs[0][i][2]), outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                        outputs[0][i][2], outputs[0][i][3]]
                    boxes.append(box)
                    scores.append(maxScore)
                    class_ids.append(maxClassIndex)

            result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45, 0.5)
            detections = []
            for i in range(len(result_boxes)):
                index = result_boxes[i]
                box = boxes[index]
                detection = {
                    'class_id': class_ids[index],
                    'class_name': CLASSES[class_ids[index]],
                    'confidence': scores[index],
                    'box': box,
                    'scale': scale}
                # ditections 내부에 dections 정보 다 포함되어 있음
                
                # detections.append(detection)
                
                #박스 작업 
                draw_bounding_box(frame, class_ids[index], scores[index], round(box[0] * scale), round(box[1] * scale),
                                round((box[0] + box[2]) * scale), round((box[1] + box[3]) * scale))

                # output 저장
                # self.out.write(frame)
        
                feelings.append(detection['class_name'])
            # Encode the frame as a JPEG image and send it to the client
            success, image = cv2.imencode('.jpg', frame)
            if not success:
                break
            feelcount=Counter(feelings)
            
            image_bytes = image.tobytes()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            await self.send(json.dumps({
                'image':image_base64,
                'feelings':feelcount
            }))
            self.feelcount=feelcount
            await asyncio.sleep(0.05)



    async def receive(self, text_data):
        message = text_data
        if message == 'start':
            self.is_streaming = True
            self.stopped = False
            self.task=asyncio.create_task(self.stream_video())
        elif message == 'stop':
            if hasattr(self.task,'cancel') :
                self.task.cancel()
                print("task cancel")
            await self.stop_streaming()
            await set_detectdedemotions(self.detected_emotions,self.feelcount)
            
            
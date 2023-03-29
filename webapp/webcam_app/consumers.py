import cv2
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
import numpy as np
from pathlib import Path
import json
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import base64
from collections import Counter
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from datetime import datetime
from .models import Counseling, Detected
from channels.db import database_sync_to_async

BASE_DIR = Path(__file__).resolve().parent
CLASSES = ['anger','anxiety','embarrassed','hurt','neutral','pleasure','sad']
# 색상 랜덤하게 뽑아서 적용 다 다르게 

colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))


def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = f'{CLASSES[class_id]} ({confidence:.2f})'
    color = colors[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    

# 모델 불러오기 
model = cv2.dnn.readNet(str(BASE_DIR)+"/best.onnx")

class VideoConsumer(AsyncWebsocketConsumer):
    
    @database_sync_to_async
    def save_detected_data(self, cost, feelings):
        now = datetime.now()
        name = f'{now.year}/{now.month}/{now.day}/{now.hour}/{cost.customername}'

        detected_data = Detected(
            cost=cost,
            name=name,
            anger=feelings.get('anger', 0),
            anxiety=feelings.get('anxiety', 0),
            embarrassed=feelings.get('embarrassed', 0),
            hurt=feelings.get('hurt', 0),
            neutral=feelings.get('neutral', 0),
            pleasure=feelings.get('pleasure', 0),
            sad=feelings.get('sad', 0)
        )
        detected_data.save()
    
    
    
    
    
    
    async def stop_streaming(self):
        self.stopped = True
        self.is_streaming = False
        self.video_capture.release()

    
    async def connect(self):
        await self.accept()
        self.video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.frame_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)
        self.is_streaming = False
        self.stopped = False

    async def disconnect(self,close_code):
            self.is_streaming = False
            self.stopped = True
        
    
  
            
    async def stream_video(self,cost):
        feelings=[]
        
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # out = cv2.VideoWriter('output.mp4', fourcc, 30, (self.frame_width, self.frame_height))
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
                # out.write(frame)
        
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

            await asyncio.sleep(0.05)




    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        counseling_id = data.get('counseling_id')
        try:
            cost = Counseling.objects.get(pk=counseling_id)
        except Counseling.DoesNotExist:
            cost = None
        if message == 'start':
            self.is_streaming = True
            self.stopped = False
            asyncio.create_task(self.stream_video(cost))
        elif message == 'stop':
            await self.stop_streaming()
            
            
            if cost is not None:
                feelcount=await self.stream_video(cost)
                await self.save_detected_data(cost, feelcount) 
# 🍃 realtime-detection-and-recognize-facial-expression

###   🗓️ 기간 : 23.03.13~23.04.07

## 서비스 : [https://emo-ai.com](https://emo-ai.com)

## 주제 : 실시간으로 대상자의 안면 감정을 인식하고 해당 정보를 저장하는 웹 프로젝트

### 프로젝트 개요 
  - 생체 데이터에 대한 폭넓은 활용
  - 상담자의 주관적인 판단에 비해 보다 객관적인 판단 가능
  - 딥러닝을 활용한 실시간 디텍션 & 감정인식
  - 온라인 면접, 상담 등 안면감정정보 수요가 있을거라 예측
  - 실시간 데이터 적재 뿐만 아니라 저장된 영상에 대해서도 활용 가능

> 특정 목표
  - AI HUB 한국인 감정인식을 위한 복합 영상의 사진 공개 데이터 세트를 활용하여 face recognition detection 모델 학습
  - Django를 활용한 백엔드 개발
  - AWS를 통한 배포 및 운영
  - 실시간 서비스를 위한 모델 최적화
  - RESTful API 설계
  - 확장가능한 설계
  
### Dataset Google Drive
- https://drive.google.com/drive/folders/1heKfk2ZYwuIufBKBLUPeWKkb6RhMJmGi?usp=share_link
- img_resize_labeling/facedata.yaml for training yolo
  
### 기술스택
  - front & backend : Django, bootstrap, css, html, javascript (이재영, 전현준, 정제경, 주한솔)  
  - machine learning : python, pytorch, yolo-v8, opencv (남정우, 최세현)  
  - architecture : aws ec2, aws alb, aws rds, aws acm, aws route53, nginx, daphne, mysql, docker (남정우)

# 팀원
- 남정우, 이재영, 정제경, 전현준, 주한솔, 최세현

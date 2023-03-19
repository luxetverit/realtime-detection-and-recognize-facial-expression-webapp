import os 
import cv2
import json
import numpy as np
hwtoeng_list=["분노","불안","당황","상처","기쁨","슬픔","중립"]


feeling={
    "분노":"0",
    "불안":"1",
    "당황":"2",
    "상처":"3",
    "중립":"4",
    "기쁨":"5",
    "슬픔": "6"
}


hwtoeng={
    "분노":"anger",
    "불안":"anxiety",
    "당황":"embarrassed",
    "상처":"hurt",
    "중립":"neutral",
    "기쁨":"pleasure",
    "슬픔": "sad"
}


checkpoint="중립"  #  <=  감정 수정
number='1'    # <=폴더 번호 수정
datatype='valid' # <= train or valid

check = hwtoeng.get(checkpoint)
  



# save_path=f"./{datatype}/"+check+"/"  #<= 미리 만들어두세요 ex ) train/anger 
# image_base_path="./Validation/images/" +check +number +'/'
# annotation_path=f"./Validation/labels/{check}.json"





"""        
YOLO 포맷은 [x_center, y_center, width, height] 를 따름 
        
"""
            


def labelmaker():
    #  "분노","불안","당황","상처","기쁨","슬픔","기쁨","중립"
    hwtoeng_list=[]
    for i in hwtoeng_list :
        checkpoint=i  #  <=  감정 수정
        number='1'    # <=폴더 번호 수정
        datatype='train' # <= train or valid

        check = hwtoeng.get(checkpoint)
        



        save_path=f"./{datatype}/"+check+number+"/"  #<= 미리 만들어두세요 ex ) train/anger 
        image_base_path="./Training/images/" +check +number +'/'
        annotation_path=f"./Training/labels/{check}.json"





        with open(annotation_path,'r') as json_file:
            json_object = json.load(json_file)
            os.mkdir(save_path+"labels")
            os.mkdir(save_path+"images")

            newlabel=save_path+"labels"+"/"
            newimgpath=save_path+"images/"
        image_count=0 
        
        for j in json_object :
            
            
            imagename=j.get('filename')
            file_list = os.listdir(image_base_path)
        
            if imagename[-2:] =="eg":
                continue
            if imagename in file_list :
            
                
                #A annotation 기준으로 받음
                total_info=j.get('annot_A')
                boxes= total_info.get('boxes')
                feeling_class=checkpoint


                #boxese
                maxX=float(boxes.get('maxX'))
                minX=float(boxes.get('minX'))
                maxY=float(boxes.get('maxY'))
                minY=float(boxes.get('minY'))

                #중심 좌표 및 박스 크기 
                box_w=maxX-minX
                box_h=maxY-minY

                xcenter=float(maxX+minX)/2
                ycenter=float(maxY+minY)/2


                #파일 읽기
                full_path=image_base_path+imagename

                img_array = np.fromfile(full_path, np.uint8) 
                img = cv2.imdecode(img_array,  cv2.IMREAD_COLOR)

                

                #파일 높이 ,길이
                img_height=img.shape[0]
                img_width=img.shape[1]

                #상대 위치 
                rel_x=str(float(xcenter/img_width))
                rel_y=str(float(ycenter/img_height))
                rel_w=str(float(box_w/img_width))
                rel_h=str(float(box_h/img_height))

                string_bbox=feeling.get(feeling_class)+" "+rel_x+" "+rel_y+" "+rel_w+" "+rel_h   

                #사이즈 맞춰 저장하기 
                wh_ratio = img_height/img_width 
                inputsize=640

                resized=cv2.resize(img,dsize=(inputsize, int(inputsize*wh_ratio)),interpolation=cv2.INTER_AREA)

                #파일 저장 
                save_image_name=hwtoeng.get(feeling_class)+str(image_count)

                cv2.imwrite(newimgpath+save_image_name+".jpg",resized)
                with open(newlabel+save_image_name+".txt","w",encoding="utf-8") as f:
                    f.write(string_bbox)


                image_count+=1     
        print("Total Image : ", image_count)

    
    
if __name__ == "__main__":
    labelmaker()

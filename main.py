import os
import pickle
import cv2 as cv
import numpy as np
from datetime import datetime
import face_recognition
import firebase_admin
from firebase_admin import db, credentials, storage

cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://stuattend-default-rtdb.firebaseio.com/",
        "storageBucket": "stuattend.appspot.com",
    })

bucket=storage.bucket()

cap=cv.VideoCapture(0)

cap.set(3,640) #set height of webcam
cap.set(4,480) #set width of webcam

# attendence background template
background_img=cv.imread('resources/background.png')


# importing mode imgs in mode_img_list
modes_folder_path='resources/Modes'
modespathlist=os.listdir(modes_folder_path)
mode_img_list=[]

for i in os.listdir(modes_folder_path):
    mode_img_list.append(cv.imread(os.path.join(modes_folder_path,i)))

print(mode_img_list[0].shape)
print(len(mode_img_list))


# load the pkl file
file = open("encodings.pkl", "rb")
encodings_list_with_ids = pickle.load(file)
student_img_list, student_id = encodings_list_with_ids
file.close()

print("loaded the pkl file")
print(student_id)

modeType=0
counter=0
id=-1
imgStudent=[]

while True:
    success,frame=cap.read()

    # resizing the img so as to reduce computation
    imgS=cv.resize(frame,(0,0),None,0.25,0.25)
    imgS=cv.cvtColor(imgS,cv.COLOR_BGR2RGB)

    # finding curr frame encodings and then comparing with the student img encodings

    # getting location of img in webcam frame
    curr_frame_location=face_recognition.face_locations(imgS)

    # encodings of webcam frame
    curr_frame_encodings=face_recognition.face_encodings(imgS,curr_frame_location)

    # background img pr webcam set or overlapped
    background_img[162:162+480,55:55+640]=frame 
    background_img[44:44+633,808:808+414]=mode_img_list[modeType] 

    # width phle then height
    if curr_frame_location:
        for encodeFace,encodeLocation in zip(curr_frame_encodings,curr_frame_encodings):
            matches=face_recognition.compare_faces(student_img_list,encodeFace)
            faceDist=face_recognition.face_distance(student_img_list,encodeFace)
            # print('matches ',matches)
            # print('faceDist ',faceDist)
            matchIndex=np.argmin(faceDist)
            id = student_id[matchIndex]
            if matches[matchIndex]:
                print(f'face detected! {student_id[matchIndex]}')

                if counter==0:
                    counter=1
                    modeType=1
                    

        if counter!=0:
            if counter==1:
                # get data
                student_info=db.reference(f'student/{id}').get()
                print(student_info)

                blob=bucket.get_blob(f'images/{id}.png')
                print(f"images/{id}.png")
                array=np.frombuffer(blob.download_as_string(),np.uint8)
                imgStudent=cv.imdecode(array,cv.COLOR_BGRA2RGB)

                # updating the attendance
                ref=db.reference(f'student/{id}')
                student_info['total_attendance']+=1
                ref.child("total_attendance").set(student_info["total_attendance"])

                datetimeObject = datetime.strptime(student_info['last_attendance_time'],
                                                    "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    student_info['total_attendance'] += 1
                    ref.child('total_attendance').set(student_info['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    background_img[44:44 + 633, 808:808 + 414] = mode_img_list[modeType]
            if modeType!=3:
                if 10 < counter < 20:
                    modeType = 2

                background_img[44:44 + 633, 808:808 + 414] = mode_img_list[modeType]

                if counter<=10:
                    cv.putText(background_img,str(student_info['total_attendance']),(861,125),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    cv.putText(background_img, str(student_info['major']), (1006, 550),
                                            cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv.putText(background_img, str(id), (1006, 493),
                                cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv.putText(background_img, str(student_info['standing']), (910, 625),
                                cv.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv.putText(background_img, str(student_info['year']), (1025, 625),
                                cv.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv.putText(background_img, str(student_info['starting_year']), (1125, 625),
                                cv.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv.getTextSize(student_info['name'], cv.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv.putText(background_img, str(student_info['name']), (808 + offset, 445),
                        cv.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                # background_img[175:175 + 216, 909:909 + 216] = imgStudent
                counter+=1

                if counter>=20:
                    counter=0
                    modeType=0
                    student_info=[]
                    imgStudent=[]
                    background_img[44 : 44 + 633, 808 : 808 + 414] = mode_img_list[modeType]

        # cv.imshow('webcam',img)

        # combined background_img+webcam

        #     print('opening webcam')
        #     cv.imshow('blank',frame)
        #     print('opened webcam')
    else:
        modeType=0
        counter=0
    cv.imshow('blank',background_img)

    if cv.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv.destroyAllWindows()

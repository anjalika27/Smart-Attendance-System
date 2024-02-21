import face_recognition
import cv2 as cv
import pickle
import os


import firebase_admin
from firebase_admin import db,credentials,storage

cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://stuattend-default-rtdb.firebaseio.com/",
        "storageBucket": "stuattend.appspot.com"
    },
)

# face_recognition takes rgb image where as opencv takes bgr image

folder_path='images/'
img_path_list=os.listdir(folder_path)

student_img_list=[]
student_id=[]

# getting student id and img in list
for path in img_path_list:
    img = cv.imread(os.path.join(folder_path, path))


    img=cv.resize(img,(216,216))
    student_img_list.append(img)
    student_id.append(os.path.splitext(path)[0]) #separates .png 

    fileName = f"{folder_path}{path}"
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

# finding encodings for each student img
def findEncodings(student_img_list):
    encoded_img_list=[]
    for img in student_img_list:
        # img=cv.resize(img,(120,160))
        img=cv.cvtColor(img,cv.COLOR_BGR2RGB)
        encoded_img_list.append(face_recognition.face_encodings(img)[0])
    return encoded_img_list


encodings_list=findEncodings(student_img_list)
print('encoding completed!')

encodings_list_with_ids=[encodings_list,student_id]

# save the encodings to file as pkl
file=open('encodings.pkl','wb')
pickle.dump(encodings_list_with_ids,file)
file.close()
print('pickling done')

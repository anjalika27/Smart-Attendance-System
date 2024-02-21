import cv2 as cv

img = cv.imread(r"images\16.jpg")
img=cv.resize(img,(216,216))
print(img.shape)
cv.imshow('img',img)
cv.waitKey(0)

# cap=cv.VideoCapture(0)
# cap.set(3,640)
# cap.set(4,480)

# while(cap.isOpened()):
#     success,img=cap.read()

#     if not success:
#         print("CAN'T CAPTURE FRAME..............")
#         break


#     cv.imshow('img',img)

#     # key=cv.waitKey(1)
#     # if key==27:
#         # break
#     if(cv.waitKey(1) & 0xFF == ord('q')):
#         break


# cap.release()
# cv.destroyAllWindows()

# enroll.py
import cv2, os, time, sys
name = sys.argv[1] if len(sys.argv)>1 else "you"
cap = cv2.VideoCapture(0)
face = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
os.makedirs(f"data/known/{name}", exist_ok=True)
count=0
while count<30:
    ok,frame=cap.read();  gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=face.detectMultiScale(gray,1.2,5,minSize=(80,80))
    for (x,y,w,h) in faces:
        roi=cv2.resize(gray[y:y+h,x:x+w],(200,200))
        cv2.imwrite(f"data/known/{name}/{int(time.time()*1000)}.png",roi)
        count+=1; cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow("enroll",frame)
    if cv2.waitKey(1)&0xFF==ord('q'):break
cap.release(); cv2.destroyAllWindows()
print("Saved",count,"images to",f"data/known/{name}")

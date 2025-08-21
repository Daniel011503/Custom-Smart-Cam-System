# train.py
import cv2, os, numpy as np, glob
X, y, labels = [], [], []
for i,person in enumerate(sorted(os.listdir("data/known"))):
    p=f"data/known/{person}"
    if not os.path.isdir(p): continue
    for fn in glob.glob(p+"/*.png"):
        X.append(cv2.imread(fn,0)); y.append(i)
    labels.append(person)
rec=cv2.face.LBPHFaceRecognizer_create()
rec.train(X, np.array(y))
os.makedirs("models",exist_ok=True)
rec.write("models/lbph.yml")
open("models/labels.txt","w").write("\n".join(labels))
print("Labels:",labels)

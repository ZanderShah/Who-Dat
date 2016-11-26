from facerec.feature import Fisherfaces
from facerec.classifier import NearestNeighbor
from facerec.model import PredictableModel
from PIL import Image
import numpy as np
from PIL import Image
import sys, os
import time
import cv2
import multiprocessing

model = PredictableModel(Fisherfaces(), NearestNeighbor())

vc = cv2.VideoCapture(0)
#Choosing the haar cascade for face detection
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt_tree.xml')

#Reads the database of faces
def readImages(path):
    sz = (256, 256)
    # Reads the images in a given folder, resizes images on the fly if size is given.
    # Returns a [Images Indices Folder_Names] list
    c = 0
    X, y = [], []
    folderNames = []
    
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            folderNames.append(subdirname)
            subjectPath = os.path.join(dirname, subdirname)
            for filename in os.listdir(subjectPath):
                try:
                    im = cv2.imread(os.path.join(subjectPath, filename), cv2.IMREAD_GRAYSCALE)
                    # Resize to (256, 256)
                    if (sz is not None):
                        im = cv2.resize(im, sz)
                    X.append(np.asarray(im, dtype=np.uint8))
                    y.append(c)
                except IOError, (e, s):
                    print "I/O error({0}): {1}".format(e, s)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
            c += 1
    return [X, y, folderNames]

#Directory of the face database
pathdir='/Users/ZanderShah/git/Project_Twice/Faces'

#Initialization:
def newFace(fileNumber):
    if not os.path.exists(os.path.join(pathdir, fileNumber)): 
        os.makedirs(os.path.join(pathdir, fileNumber))

    while (1):
        ret, frame = vc.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 3)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow('Recognition', frame)
        
        if cv2.waitKey(10):
            break

    cv2.destroyAllWindows()

    start = time.time()
    c = 0

    for i in xrange(50):
        ret,frame = vc.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 3)

        for (x, y, w, h) in faces:
            c += 1
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            destination = os.path.join(pathdir, os.path.join(fileNumber, os.path.join(str(time.time() - start) + '.jpg')))
            cv2.imwrite(destination, cv2.resize(gray[y : y + h, x : x + w], (273, 273)));
        cv2.imshow('Recognition', frame)
        cv2.waitKey(10)
    cv2.destroyAllWindows()

[X, y, subjectNames] = readImages(pathdir)
labels = list(xrange(max(y)+1))

subjects = dict(zip(labels, subjectNames))
model.compute(X, y)

#Start recognition
while (1):
    rval, frame = vc.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 3)

    for (x, y, w, h) in faces:
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        sampleImage = gray[y : y + h, x : x + w]
        sampleImage = cv2.resize(sampleImage, (256, 256))

        [predictedLabel, prediction] = model.predict(sampleImage)

        if int(prediction['distances']) <=  1000:
            cv2.putText(frame, 'You are : ' + str(subjects[predictedLabel]), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 250), 3, 1)
    
    cv2.imshow('result', frame)
    if cv2.waitKey(10) == 27:
        break

cv2.destroyAllWindows()
vc.release()
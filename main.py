from facerec.feature import Fisherfaces
from facerec.feature import PCA
from facerec.feature import Identity
from facerec.classifier import NearestNeighbor
from facerec.preprocessing import TanTriggsPreprocessing
from facerec.operators import ChainOperator
from facerec.model import PredictableModel

import numpy as np
from PIL import Image
import sys, os
import cv2
import multiprocessing

#Webcam
vc=cv2.VideoCapture(0)

#Directory for face database that we are comparing to
databasedir = ''

#Creating the default comparison models
fisherModel = PredictableModel(Fisherfaces(), NearestNeighbor())
PCAModel = PredictableModel(PCA(), NearestNeighbor())
IdentityModel = PredictableModel(Identity(), NearestNeighbor())

#Using default haarcascade
face_cascade = cv2.CascadeClassifier('src/haarcascade_frontalface_default.xml')

def lockScreen(path):
    timer = 0
    while 1:
        timer += 1
        ret, frame = vc.read()
        isRecognized = True
        
        displayToScreen(frame)
        detectedFaces = facialDetection(frame)
        
        for (x,y,w,h) in detectedFaces:
            #For each of our detected faces
            resized_image = cv2.resize(frame[y:y+h, x:x+w], (256,256))

            #iterate through all the images saved in our database
            for filename in os.listdir(databasedir):
                if filename.endswith(".jpg"):
                    testImage = read_image(databasedir, filename)


                    if facialRecognition(resized_image, testImage):
                        isRecognized = True
                    else:
                        store_pic(database, resized_image)
                        isRecognized = False

        if not isRecognized:
            break
        



    return True


if __name__ == "__main__":
    result = lockScreen()
    print result

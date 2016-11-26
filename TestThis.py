#function that reads the image from the specified directory
#Returns np.asarray with datatype np.uint8
def read_image(path, filename, size=(256,256)): 
    try:
        im = cv2.imread(os.path.join(path, filename), cv2.IMREAD_GRAYSCALE)

        if (size is not None):
            im = cv2.resize(im, size)

        return im

    except IOError, (errnum, strerror):
        print "I/O error({0}: {1})".format(errnum, strerror)
    except:
        print "Unexpected error: ", sys.exc_info()[0]
        raise


def facialDetection(path, frame):
    #first converts image to grayscale so it is easier to work with
    grayScaleImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    #faces is an array of dimensions representing the faces detected by the haar cascade
    faces = face_cascade.detectMultiScale(gray, 1.2, 3)

    return faces

    
def store_pic(path, image):
    cv2.imwrite(path+'/'+str(time.time()) + '.jpg', image)


def facialRecognition( image1, image2 ):
    
def displayToScreen(frame):
    cv2.imshow('WhoDat',frame) 

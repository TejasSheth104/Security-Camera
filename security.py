import cv2

# start video capture
camera = cv2.VideoCapture(0)
# check if cv2 has started the camera or not
while camera.isOpened():
    # detects the camera 
    # ret, frame = camera.read()
    ret, frame1 = camera.read()
    ret, frame2 = camera.read()

    # difference between 2 frames to detect motion
    frameDifference = cv2.absdiff(frame1, frame2)

    # turn the frame differnece from colored to gray scale
    grayImg = cv2.cvtColor(frameDifference, cv2.COLOR_BGR2GRAY)

    # blur, pass gray, kernel size, and sigmax as 0
    blurImg = cv2.GaussianBlur(grayImg, (5,5), 0)

    #get rid of noise using threshold, gives sharper and brighter image
    _, thresh = cv2.threshold(blurImg, 20, 255, cv2.THRESH_BINARY)

    # dilation makes noiseless actual things a little bit bigger 
    dilated = cv2.dilate(thresh, None, iterations=3)
    
    # find possible contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # to see/draw the contours as output
    cv2.drawContours(frame1, contours, -1, (0,255,255), 2)

    # check if user presses the proper key to quit, ord fetches unicode value of the parameter passed
    if cv2.waitKey(10) == ord('q'):
        break
    # display 
    # cv2.imshow('Camera Feed', frame)
    # cv2.imshow('Camera Feed', frameDifference)
    # cv2.imshow('Camera Feed', grayImg)
    # cv2.imshow('Camera Feed', blurImg)
    # cv2.imshow('Camera Feed', thresh)
    # cv2.imshow('Camera Feed', dilated)
    cv2.imshow('Camera Feed', frame1)



    
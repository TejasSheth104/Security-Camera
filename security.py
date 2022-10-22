import cv2
import winsound

# 
font = cv2.FONT_HERSHEY_SIMPLEX
# start video capture
camera = cv2.VideoCapture(0)
# check if cv2 has started the camera or not
while camera.isOpened():
    # detects the camera 
    # ret, frame = camera.read()
    ret, frame1 = camera.read() # prev postion
    ret, frame2 = camera.read() # current position

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

    # to see/draw the all possible contours as output
    # cv2.drawContours(frame1, contours, -1, (255,0,0), 2)

    # to draw select contours
    for contourSize in contours:
        # ignore smaller area contours and focus on larger movements
        if cv2.contourArea(contourSize) < 10000:
            continue
        # get coordinates of rectangle around the detected motion
        xCoord, yCoord, width, height = cv2.boundingRect(contourSize)
        # draw the rectangle based on coordinates from previous step
        cv2.rectangle(frame1, (xCoord, yCoord), (xCoord+width, yCoord+height), (0,0,255), 2)
        # cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
        cv2.putText(frame1, "Motion Detected", (200, 45), font, 1, (0, 0, 255), 2)

        # default sound (frequency, duration_ms)
        winsound.Beep(500, 200)
        # external source file
        # ASYNC - sound plays
        # winsound.PlaySound('alert.wav', winsound.SND_ASYNC)

    # check if user presses the proper key to quit, ord fetches unicode value of the parameter passed
    if cv2.waitKey(10) == ord('q'):
        break

    # display 
    cv2.imshow('Camera Feed', frame1)


    
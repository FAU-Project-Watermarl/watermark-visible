import cv2
import pytesseract
import json

# Open video file
cap = cv2.VideoCapture('shuffledWatermarkOutput.mp4')
 
# total frame count
totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# current frag time length.
fragTimeInterval = 1

with open("db.json", "r") as infile:
    db = json.load(infile)

userComboTimeLoc = 0

successCounter = 0

frameCounter = 0

userCombo = db["user1"]

prevTime = 0

# Loop through video frames, issue with the stupid ts file, sometimes it doesn't round to 1 second, subtracting 8 frames 
# will give us EDGE CASE safety.
while cap.isOpened() and cap.get(cv2.CAP_PROP_POS_FRAMES) < totalFrames - 7:
    ret, frame = cap.read()

    frameCounter += 1

    if(frameCounter % 20 != 0):
        continue
    
    height, width, _ = frame.shape
    roi = frame[0:int(height/8), 0:int(width/10)]

    # Apply image processing to enhance text visibility, who know why this works
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Extract text from frame using OCR
    text = pytesseract.image_to_string(thresh)

    # Display text on frame
    cv2.putText(frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show frame
    #cv2.imshow('Frame', roi)

    currentTime = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
    
    # we need to make 10 second intervals later down the road.
    if(int(currentTime) > int(prevTime) and currentTime != 0):
        userComboTimeLoc += 1

    if (userCombo[userComboTimeLoc].lower() in text.lower()):
        successCounter += 1
    else:
        #logs to see wtf is happening, outputted to log.txt
        with open('log.txt', 'a') as file:
        # Write string to the file[]
            file.write(f"--------TEXT START-----failed for {userCombo[userComboTimeLoc]} , location {userComboTimeLoc} -\n" + text + "--------- TEXT END ----------- \n")

    #print()
    prevTime = currentTime

    # Exit if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# print the success value divided by the total number of frames
# 98% (it's 100% pretty much for 420p all the way up to 1080p)
print("Successful extraction rate: {:.2f}%".format(successCounter/(totalFrames / 20) * 100))


db["user1"] = []

with open("db.json", "w") as outfile:
    json.dump(db, outfile)

# Release video file and close window
cap.release()
cv2.destroyAllWindows()
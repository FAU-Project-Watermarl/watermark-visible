import cv2
import pytesseract
import json
import subprocess
import numpy as np

out_ts_list = []
with open("frags/out.m3u8", "r") as file:
    lines = file.readlines()
    for line in lines:
        if ".ts" in line:
            sanitized_line = line.replace(" ", "").strip() 
            out_ts_list.append(sanitized_line)

with open("db.json", "r") as infile:
    db = json.load(infile)

output_dir = "frags"

totalFramesTested = 0

userListLoc = 0

successCounter = 0

size_ratio = 3

failed_attempts = 0

userCombo = db["user1"]

fps = db["fps"]

pix_width = db["pix_width"]

pix_height = db["pix_height"]

with open('log.txt', 'w') as file:
        file.write(f" ")

for ts_file in out_ts_list:

    try:
        completed_process = subprocess.run(f"ffmpeg -y -i frags/{ts_file} -c:v copy -c:a copy temp_ts.mp4", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        userListLoc += 1
        with open('ts_log.txt', 'a') as file:
            file.write(str(e)+ "\n")
        continue
    
    cap = cv2.VideoCapture('temp_ts.mp4')
 
    totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frameCounter = 0
    
    while cap.isOpened() and cap.get(cv2.CAP_PROP_POS_FRAMES) < totalFrames - 7:
        ret, frame = cap.read()

        frameCounter += 1

        if(frameCounter % int(fps/2) != 0):
            continue
        
        totalFramesTested += 1

        height, width, _ = frame.shape
        
        roi = frame[0:pix_height, 0:pix_width]
        # print(roi)

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        text = pytesseract.image_to_string(thresh)

        cv2.putText(frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Frame', roi)

        currentTime = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

        if (userCombo[userListLoc].lower() in text.lower()):
            successCounter += 1
        else:
            if(size_ratio < 7):
                failed_attempts += 1
                if(failed_attempts == 7):
                        failed_attempts = 0
                        size_ratio += 1
            with open('log.txt', 'a') as file:
                file.write(f"--------TEXT START-----failed for {userCombo[userListLoc]} , location {userListLoc} -\n" + text + "--------- TEXT END ----------- \n")

        prevTime = currentTime

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    userListLoc += 1

with open('extract.txt', 'w') as file:
    file.write("Successful extraction rate: {:.2f}%".format((successCounter/totalFramesTested) * 100))

with open("db.json", "w") as outfile:
    json.dump(db, outfile)

cap.release()
cv2.destroyAllWindows()
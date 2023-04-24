import subprocess
import uuid
import cv2
import pytesseract
import json
import random
import ffmpeg

# some distinct watermark
textOverlayA = 'XYZ'

# manuel, change the input here based on the outputted resolultion from above.
# Define FFmpeg command
applyWatermarkA = (f'ffmpeg -y -i input.mp4 -filter_complex '
              f'"[0:v]drawtext=fontfile=arial.ttf:fontsize=36:text=\'{textOverlayA}\':'
              f'x=10:y=10:fontcolor=white@1.0:box=1:boxcolor=black@1.0,'
              f'format=yuva444p[text];[0:v][text]overlay=10:10"'
              f' -c:a copy watermarkedVideoA.mp4')

subprocess.run(applyWatermarkA, shell=True)

textOverlayB = 'UVW'

# Define FFmpeg command
applyWatermarkB = (f'ffmpeg -y -i input.mp4 -filter_complex '
              f'"[0:v]drawtext=fontfile=arial.ttf:fontsize=36:text=\'{textOverlayB}\':'
              f'x=10:y=10:fontcolor=white@1.0:box=1:boxcolor=black@1.0,'
              f'format=yuva444p[text];[0:v][text]overlay=10:10"'
              f' -c:a copy watermarkedVideoB.mp4')

# Run FFmpeg command
subprocess.run(applyWatermarkB, shell=True)

# maneul, use this preset for higher res
#highestResolutionB = f'ffmpeg -i watermarkedVideoB.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease" -c:a copy highWatermarkedVideoB.mp4'

#subprocess.run(highestResolutionB, shell=True)

# maneul, use this preset for higher res
#highestResolutionA = f'ffmpeg -i watermarkedVideoA.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease" -c:a copy highWatermarkedVideoA.mp4'

#subprocess.run(highestResolutionA, shell=True)

# manuel, use this preset for lower res
lowestResolutionB = f'ffmpeg -y -i watermarkedVideoB.mp4 -vf "scale=-2:420:force_original_aspect_ratio=decrease" lowWatermarkedVideoB.mp4'

subprocess.run(lowestResolutionB, shell=True)

# manuel, use this preset for lower res
lowestResolutionA = f'ffmpeg -y -i watermarkedVideoA.mp4 -vf "scale=-2:420:force_original_aspect_ratio=decrease" lowWatermarkedVideoA.mp4'


subprocess.run(lowestResolutionA, shell=True)


# split the input file into fMP4 segments using FFmpeg
fragmentA = f'ffmpeg -y -i lowWatermarkedVideoA.mp4 -c:v h264 -flags +cgop -g 30 -hls_time 1 fragA.m3u8'
subprocess.run(fragmentA, shell=True)

fragmentB = f'ffmpeg -y -i lowWatermarkedVideoB.mp4 -c:v h264 -flags +cgop -g 30 -hls_time 1 fragB.m3u8'

# select a frag of random type A or B
subprocess.run(fragmentB, shell=True)

with open("db.json", "r") as infile:
    db = json.load(infile)

userCombo = db["user1"]

frags = []
for i in range(0,7):
    selectChoice = random.choice([0,1])
    if(selectChoice == 0):
        selectedFragment = 'fragA'+ str(i) +'.ts'
        userCombo.append(textOverlayA)
    else:
        selectedFragment = 'fragB'+ str(i) +'.ts'
        userCombo.append(textOverlayB)
    frags.append(selectedFragment)

with open("db.json", "w") as outfile:
    json.dump(db, outfile)


with open("out.m3u8", "w") as f:
    f.write("#EXTM3U\n")
    f.write("#EXT-X-VERSION:3\n")
    f.write("#EXT-X-MEDIA-SEQUENCE:0\n")
    f.write("#EXT-X-INDEPENDENT-SEGMENTS\n")
    f.write("#EXT-X-DISCONTINUITY-SEQUENCE:1\n")
    for i in range(0,7):
        f.write("#EXTINF:1.000000,\n")
        f.write(frags[i]+ '\n')

    f.write("#EXT-X-ENDLIST\n")
f.close()

shuffleFrags = f'ffmpeg -y -protocol_whitelist "file,http,https,tcp,tls" -i out.m3u8 -c copy shuffledWatermarkOutput.mp4'
subprocess.run(shuffleFrags, shell=True)


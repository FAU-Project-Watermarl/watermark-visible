import subprocess
import cv2
import json
import random
import os

input_video = "input4.mp4"

output_dir = "frags"

older_exists = os.path.exists(output_dir)
if(older_exists):
    subprocess.run(f"rm -rf ./{output_dir}", shell=True)

os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(input_video)
total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)
duration = total_frames / fps

get_resolution = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of json {input_video}'
result = subprocess.run(get_resolution, shell=True, capture_output=True, text=True)
resolution_data = json.loads(result.stdout)

width = resolution_data["streams"][0]["width"]
height = resolution_data["streams"][0]["height"]
    
reference_resolution = (width, height)

textOverlayA = "ABC"
textOverlayB = "UVW"

applyWatermarkA = (
    f'ffmpeg -y -i {input_video} -filter_complex '
    f'"[0:v]drawtext=fontfile=arial.ttf:fontsize={40}:'
    f'text=\'{textOverlayA}\':x=10:y=10:fontcolor=white@1.0:box=1:boxcolor=black@01.0:'
    f'boxborderw=8,format=yuva444p[text];[0:v][text]overlay=10:10"'
    f' -c:a copy watermarkedVideoA.mp4'
)
subprocess.run(applyWatermarkA, shell=True)

applyWatermarkB = (
    f'ffmpeg -y -i {input_video} -filter_complex '
    f'"[0:v]drawtext=fontfile=arial.ttf:fontsize={40}:'
    f'text=\'{textOverlayB}\':x=10:y=10:fontcolor=white@1.0:box=1:boxcolor=black@1.0:'
    f'boxborderw=8,format=yuva444p[text];[0:v][text]overlay=10:10"'
    f' -c:a copy watermarkedVideoB.mp4'
)
subprocess.run(applyWatermarkB, shell=True)

# # maneul, use this preset for higher res
# highestResolutionB = f'ffmpeg -y -i watermarkedVideoB.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease" -c:a copy highWatermarkedVideoB.mp4'

# subprocess.run(highestResolutionB, shell=True)

# # maneul, use this preset for higher res
# highestResolutionA = f'ffmpeg -y -i watermarkedVideoA.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease" -c:a copy highWatermarkedVideoA.mp4'

# subprocess.run(highestResolutionA, shell=True)

# manuel, use this preset for lower res
lowestResolutionB = f'ffmpeg -y -i watermarkedVideoB.mp4 -vf "scale=-2:420:force_original_aspect_ratio=decrease" lowWatermarkedVideoB.mp4'
subprocess.run(lowestResolutionB, shell=True)

# manuel, use this preset for lower res
lowestResolutionA = f'ffmpeg -y -i watermarkedVideoA.mp4 -vf "scale=-2:420:force_original_aspect_ratio=decrease" lowWatermarkedVideoA.mp4'
subprocess.run(lowestResolutionA, shell=True)


# split the input file into fMP4 segments using FFmpeg
fragmentA = f'ffmpeg -y -i watermarkedVideoA.mp4 -c:v h264 -flags +cgop -g 30 -hls_time 1 {output_dir}/fragA.m3u8'
subprocess.run(fragmentA, shell=True)

fragmentB = f'ffmpeg -y -i watermarkedVideoB.mp4 -c:v h264 -flags +cgop -g 30 -hls_time 1 {output_dir}/fragB.m3u8'
subprocess.run(fragmentB, shell=True)

with open("db.json", "r") as infile:
    db = json.load(infile)

userCombo = db["user1"]

frags = []

tempUserCombo = []
for i in range(0,int(duration)):
    selectChoice = random.choice([textOverlayA,textOverlayB])
    if(selectChoice == textOverlayA):
        selectedFragment = 'fragA'+ str(i) +'.ts'
    else:
        selectedFragment = 'fragB'+ str(i) +'.ts'

    userCombo.append(selectChoice)
    frags.append(selectedFragment)

db["fps"] = fps

with open("db.json", "w") as outfile:
    json.dump(db, outfile)

with open(f"{output_dir}/out.m3u8", "w") as f:
    f.write("#EXTM3U\n")
    f.write("#EXT-X-VERSION:3\n")
    f.write("#EXT-X-MEDIA-SEQUENCE:0\n")
    f.write("#EXT-X-INDEPENDENT-SEGMENTS\n")
    f.write("#EXT-X-DISCONTINUITY-SEQUENCE:1\n")
    for i in range(0,int(duration)):
        f.write("#EXTINF:1.000000,\n")
        f.write(frags[i]+ '\n')

    f.write("#EXT-X-ENDLIST\n")
f.close()


shuffleFrags = f'ffmpeg -y -protocol_whitelist "file,http,https,tcp,tls" -i  {output_dir}/out.m3u8 -c copy shuffledWatermarkOutput.mp4'
subprocess.run(shuffleFrags, shell=True)
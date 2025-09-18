import cv2
import pytesseract

video = cv2.VideoCapture("Webite Task - SD 480p.mov")
frame_rate = 1  # 1 frame/sec
count = 0

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    if count % int(video.get(5)) == 0:
        crop = frame[int(frame.shape[0]*0.75):]  # bottom 25% of frame
        text = pytesseract.image_to_string(crop)
        if text.strip():
            print(text.strip())
    count += 1

video.release()
gf
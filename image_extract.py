import cv2
# import subprocess

# open the video file
# subprocess.call('ffmpeg -i Rutting_4K60fps.mov -ss 00:00:46 -to 00:00:53 -c copy output.mp4', shell = True)
for num in range(6,10):
    videoName_new = 'train_0' + str(num) + '.mp4'
    cap = cv2.VideoCapture(videoName_new)
    i = 1
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        else:
            cv2.imwrite('train_0' + str(num) + '_' + str(i).zfill(5) + '.jpg', frame)
            i += 1
    cap.release()
cv2.destroyAllWindows()

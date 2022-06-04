import cv2
import time

#Capture webcam in a duration (seconds), export video to 'video/output.avi'
def record_webcam(capture_duration):
    cap = cv2.VideoCapture(0)

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = 30

    out = cv2.VideoWriter('video/output.avi', cv2.VideoWriter_fourcc('M','J','P','G'), fps, (frame_width,frame_height))

    start_time = time.time()
    while(time.time() - start_time <= capture_duration):
        ret, frame = cap.read()

        if ret == True:
            # Write the frame into the file 'output.avi'
            out.write(frame)
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

#Show a video
def show_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if cap.isOpened() == False:
        print('Error opening ', video_path)

    while (cap.isOpened()):
        ret, frame = cap.read()

        if ret == True:
            cv2.imshow(str(video_path), frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    record_webcam(capture_duration = 5)
    print('Video exported to video/output.avi')
    show_video('video/output.avi')
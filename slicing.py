import os
import cv2

from subprocess import Popen, PIPE

_stride = 2

def main():
    task = "Suturing"
    CWD = os.path.dirname(os.path.realpath(__file__))
    image_dir = os.path.join(CWD, task,"images")
    video_dir = os.path.join(CWD, task,"videos")
    slice_task(image_dir,video_dir,DEBUG=False)


def slice_task(image_dir, video_dir, DEBUG=False):
    stride = _stride
    for root, dirs, files in os.walk(video_dir):
        for file in files:

            if "09" not in file or "Left" not in file:
                print("not using",file)
                continue
            else:
                print("using",file)
            video_fname = os.path.join(root,file)
            video_fold = os.path.basename(video_fname)
            image_fold = video_fname.replace(".avi","")
            image_fold = image_fold.replace("_Left","")
            image_fold = image_fold.replace("videos","images")

            cap = cv2.VideoCapture(video_fname)

            if not os.path.exists(image_fold):
                os.makedirs(image_fold)

            frame_data = []
            i=0
            saved_i=0
            #tf = totalFrames(video_fname)

            while cap.isOpened():
                ret, frame = cap.read()
                #print("i:",i,"\tret:",ret,"\tframe:","-","\tcap:",cap)
                if not ret:
                    print("\t\t\t\tbreak:")
                    break   
                
                if keepFrame(i,stride):
                    save_frame = os.path.join(image_fold,"frame_"+getIndexString(str(saved_i))+".png" )
                    if os.path.exists(save_frame):
                        print("already saved",save_frame, "i:",i,"ret:",ret,"cap:",cap)  
                        saved_i += 1
                        saved_i                  
                        continue
                    #frame_data.append([i , "frame_"+getIndexString(str(i)), True])
                    frame_data.append([i ,saved_i])
                    if not DEBUG:
                        cv2.imwrite(save_frame, frame) 
                        print("saved frame:",save_frame, "i:",i,"ret:",ret,"cap:",cap)
                    else:
                        print("would've written:",save_frame, "i:",i,"ret:",ret,"cap:",cap)
                    saved_i += 1        
                else: 
                    #frame_data.append([i , "frame_"+getIndexString(str(i)), ""])
                    frame_data.append([i , ""])
                #print("save_frame:",save_frame)
                i += 1               
                #cv2.imwrite('C:/Users/ianre/Desktop/coda/aws-labeling/cogito-job/slicing_tests/29s/test_'+str(i)+'.jpg', frame)
            cap.release()
            cv2.destroyAllWindows()   

def getIndexString(i):
    if len(str(i)) >= 4:
        return i
    else:
        return getIndexString("0"+i)

def keepFrame(index, stride):
    return index%stride==0

def totalFrames(filename):
    command = "C:\\FFmpeg\\bin\\ffprobe.exe -v error -select_streams v:0 -show_entries stream=nb_frames -of default=nokey=1:noprint_wrappers=1 " + filename
    total_fames = 0
    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    rc = p.returncode        
    total_fames +=  int(output)
    return total_fames




main();
#A python script that generates a gif from a random video in a youtube playlist.
from PIL import Image
from pytube import YouTube
from pytube import Playlist
import random
import cv2
import os

def img_clean(frame_initial, frame_final):
    frame_current = frame_initial
    while(frame_current <= frame_final):
        name = 'data/img/' + str(frame_current) + '.jpg'
        if os.path.exists(name):
            os.remove(name)
        frame_current+=1 

def media_clean(media_directory):

    if os.path.exists(media_directory):
        os.remove(media_directory)


def create_gif(media_name, frame_initial, frame_final):
    print("Creating gif...")
    media_video = cv2.VideoCapture('data/'+media_name+'.mp4')
    images = []
    frame_current=frame_initial
    while(frame_current<=frame_final):
        ret, frame = media_video.read()

        if ret:
            name = 'data/img/' + str(frame_current) + '.jpg'
            cv2.imwrite(name, frame)
            im=Image.open(name)
            images.append(im)
            frame_current+=1
        else:
            break
    media_duration=int(frame_final)-int(frame_initial)
    #create gif
    images[0].save(media_name+'.gif',
    save_all = True, append_images = images[1:], 
    optimize = False, duration = media_duration)    

    media_video.release()
    cv2.destroyAllWindows()   

def media_download(media_name):
    print("Downloading...")
    playlist = Playlist('https://youtube.com/playlist?list=PLD72Ylz-Y01vcGTYmEaN9nz02o0yZMWy8')

    link=random.choice(playlist.video_urls)

    yt = YouTube(link) 
    try: 
        yt.streams.filter(progressive = True, 
    file_extension = "mp4").first().download(output_path = "./data", 
    filename = media_name+".mp4")
    except: 
        print("Could not download!") 
    print('Download complete!') 

#---------------------------------------------------------------
print("-Meow to gif-")
print("It generates a short gif of a cat from a youtube video")
print("-----------------------")
media_name = input('gif file name: ')
media_frame_initial = 0
media_duration = int(media_frame_initial) + 50

def app():

    if not os.path.exists('data/'+media_name+'.mp4'):
        media_download_continue=input('a download will begin. do you wish to continue? (y/n): ')
        if(media_download_continue=='y'):
            media_download(media_name)
        else:
            return 0
    create_gif(media_name,int(media_frame_initial),int(media_duration))
    img_clean(int(media_frame_initial),int(media_duration)) 
    media_delete_continue=input('do you wish to keep the video media file? (y/n): ')
    if(media_delete_continue=='n'):
        media_clean('data/' + media_name + '.mp4')
    else:
        return 0

app()
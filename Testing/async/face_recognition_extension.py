import asyncio
import json
from datetime import datetime
from re import L
import face_recognition
import cv2
import numpy as np
import os
import glob
# import mediapipe as mp
import time

import time
import smtplib
from email.message import EmailMessage


# TODO: Specify this for multiple cam use case
video_capture = cv2.VideoCapture(0)


async def check(current_time):
    if int(current_time[-2:]) == 30 or int(current_time[-2:]) == 31 or int(current_time[-2:]) == 32:
        print("We got it")
    else:
        print("No")


async def loop(video_capture):
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()

        if process_this_frame:
            process_this_frame = not process_this_frame

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        await check(current_time)
        # ans = asyncio.create_task(check(current_time))

        # Display the resulting image
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# faces[str(input("Dectected new face. Enter name: "))] = screenshot
# updateDB(faces)
asyncio.run(loop(video_capture))

video_capture.release()
cv2.destroyAllWindows()


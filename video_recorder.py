import time

import cv2
import os

import requests

LAST_BIRD_OCCURRENCE_TIMEOUT = 5
RECORDINGS_DIRECTORY = "recordings/"
FRAME_RATE = 30


class BirdDetectionVideoHandler:
    def __init__(self, frame_width, frame_height):
        self.recording = False
        self.last_bird_occurrence = time.time() - LAST_BIRD_OCCURRENCE_TIMEOUT
        self.writer = None
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.current_file = None
        if not os.path.exists(RECORDINGS_DIRECTORY):
            os.makedirs(RECORDINGS_DIRECTORY)

    def new_recording(self, recording_id):
        print("new recording:" + recording_id)
        self.current_file = RECORDINGS_DIRECTORY + recording_id + ".avi"
        self.writer = cv2.VideoWriter(self.current_file, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                      FRAME_RATE,
                                      (self.frame_width, self.frame_height))
        self.recording = True

    def write_frame(self, frame, current_fps):
        i = 0
        while i < (FRAME_RATE / current_fps):
            self.writer.write(frame)
            i += 1

    def bird_detected(self):
        self.last_bird_occurrence = time.time()

    def is_recording(self):
        return self.recording

    def no_recent_occurrences(self):
        return time.time() - self.last_bird_occurrence > LAST_BIRD_OCCURRENCE_TIMEOUT

    def stop_and_publish(self):
        print("sending a video")
        requests.post("http://osiris.local:8000/upload",
                      files={'file': open(self.current_file, 'rb')})
        self.writer.release()
        self.recording = False

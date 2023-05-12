import streamlink, cv2
import time
import queue
import threading

# Create a queue

def stream_to_url(url, quality='best'):
    streams = streamlink.streams(url)
    if streams:
        return streams[quality].to_url()
    else:
        raise ValueError("No steams were available")
class StreamReader:
    def __init__(self,url,quality='best',fps=30.0,buffer_length=100):
        self.cam = cv2.VideoCapture(stream_to_url(url,quality))
        self._buffer_length=buffer_length
        self._init_buffer()
        self.cam_thread = threading.Thread(target=self.read_thread,daemon=True)
        self.cam_thread.start()
        self.time_interval = 1.0 / fps
        self.last = time.time()
    def _init_buffer(self):
        self._buffer = queue.Queue()
        for _ in range(self._buffer_length):
            self._buffer.put(self.cam.read(), block=True,timeout=120)
    def read_thread(self):
        while True:
            self._buffer.put(self.cam.read(),block=False,timeout=15)
            
            
    def read(self):
        while not (time.time() - self.last)>self.time_interval:
            time.sleep(0.01)
        self.last = time.time()
        return self._buffer.get()
        



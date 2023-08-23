import cv2
import pyaudio
import wave
import pathlib

class Audio():
    def __init__(self):
        self._load_url()
        self.chunk = 1024

    def _load_url(self):
        self.audio_url = list(pathlib.Path('.').glob('data\\audio\\*.wav'))
    
    def open_file(self, num):
        self.wf = wave.open(str(self.audio_url[num]), "rb")
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = self.p.get_format_from_width(self.wf.getsampwidth()),channels= self.wf.getnchannels(),rate = self.wf.getframerate(), output=True)

    def play(self):
        data = self.wf.readframes(self.chunk)

        while data != b"":
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)

    def stop(self):
        self.stream.stop_stream()

    def __del__(self):
        self.stream.close()
        self.p.terminate()

class Movie:
    def __init__(self, w, h):
       self._load_url()
       self.w = w
       self.h = h

    def _load_url(self):
        self.movie_url = list(pathlib.Path('.').glob('data\\movie\\*.mp4')) #dataフォルダにあるjpgファイルを読み込み

    def open_file(self, num):
        self.cap = cv2.VideoCapture(str(self.movie_url[num]))
        if not self.cap.isOpened():
            raise ValueError("unable to open video source", str(self.movie_url[num]))
        self.max_frame = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
   
    def stop(self):
        self.video_thread.stop()
    
    def get_frame(self):
        try:
            ret, frame = self.cap.read()
            if ret:
                re_frame = cv2.resize(frame, (self.w, self.h))
                return (ret, cv2.cvtColor(re_frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        except:
            ret = False
            frame = None
            return (ret, frame)

    def __del__(self):
        print("Memory relase")
        self.cap.release()
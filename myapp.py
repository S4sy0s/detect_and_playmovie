import tkinter as tk
import PIL.Image, PIL.ImageTk
import webcam as wc
import movie as mv
import target as tr
import threading as th
import time
import cv2

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.w = self.winfo_screenwidth()
        self.h = self.winfo_screenheight()
        self.title("Detection")
        self.state('zoomed')
        self.attributes("-fullscreen", True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.detection_frame = 0
        self.max_frame = 10
        self.detected_flag = False
        
        self.cap = wc.WebCam(self.w, self.h)
        self.target = tr.Target()
        self.audio = mv.Audio()
        self.movie = mv.Movie(self.w, self.h)

        self.pre_num = len(self.target.imgs)
        
        ### webカメラ用
        self.main_frame = tk.Frame()
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_bg = tk.Label(self.main_frame)
        self.main_bg.pack()

        ### 映像用
        self.movie_frame = tk.Frame()
        self.movie_frame.grid(row=0, column = 0, sticky = "nsew")
        self.movie_bg = tk.Label(self.movie_frame)
        self.movie_bg.pack()

        self.movie_thread = None
        self.audio_thread = None

        self.main_frame.tkraise()
        self.update()

    def changePage(self, page):
        page.tkraise()

    def update(self):
        if self.detected_flag == False:
            try:
                ret, frame, number = self.cap.get_frame()
            except:
                ret = False
                frame = 0
                number = -1

            if ret:
                if number < len(self.target.imgs):
                    if (self.pre_num == number) or (self.pre_num == len(self.target.imgs)):
                        self.detection_frame = self.detection_frame + 1
                    else:
                        self.detection_frame = 0

                    self.pre_num = number

                    ### 検出された
                    if self.detection_frame >= self.max_frame:
                        self.detected_flag = True
                        self.audio.open_file(self.pre_num)
                        self.movie.open_file(self.pre_num)
                        time.sleep(1.0)
                        self.changePage(self.movie_frame)
                        pass
                else:
                    self.detection_frame = (self.detection_frame - 1) if (self.detection_frame > 0) else 0
                    self.pre_num = len(self.target.imgs)
                
                persec = int(self.detection_frame/self.max_frame * 100)
                font_x = int(self.w * 0.1)
                font_y = int(self.h * 0.1)
                cv2.putText(frame, text=str(persec), org=(font_x, font_y), fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 2.0, color=(0, 255, 0), thickness = 5, lineType=cv2.LINE_AA)
                cv2.putText(frame, text = "%", org=(font_x + int(self.w * 0.1), font_y), fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 2.0, color = (0, 255, 0), thickness = 5, lineType = cv2.LINE_AA)
        
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                self.main_bg.config(image = self.photo)
                self.movie_bg.image = self.photo
                self.after(100, self.update)
            else:
                print("No return Cap")
            
        else:
            self.movie_thread = th.Thread(target = self._stream, daemon=True)
            self.audio_thread = th.Thread(target = self.audio.play, daemon = True)
            self.audio_thread.start()
            self.movie_thread.start()

    def _stream(self):
        for _ in range(self.movie.max_frame):
            self.play_movie()

        self.detected_flag = False
        self.detection_frame = 0
        self.pre_num = len(self.target.imgs)
        self.changePage(self.main_frame)
        self.movie_thread = None
        self.audio_thread = None
        self.after(100, self.update())

    def play_movie(self):
        ret, frame = self.movie.get_frame()
        if ret:
            self.photo2 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.movie_bg.config(image = self.photo2)
            self.movie_bg.image = self.photo2
        else:
            self.detected_flag = False
            self.detection_frame = 0
            self.pre_num = len(self.target.imgs)
            self.changePage(self.main_frame)
            self.movie_thread = None
            self.audio_thread = None
            self.after(100, self.update())
import cv2
import facedetect as fd
import target as tr

class WebCam():
    def __init__(self, w, h):
        self.facedetect = fd.FaceDetect()
        self.target = tr.Target()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("camera is unavailable")
        self.width, self.height = self._resize((self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), (w, h))
        
    def get_frame(self):
        ret, frame = self.cap.read()
        number = len(self.target.imgs)

        if ret == False: ## 読み込めない場合処理終了
            return (ret, None, number)
        
        
        output, number = self.target.detect(frame)
        output = self.facedetect.detect_draw(output)

        output = cv2.resize(output, (self.width, self.height))

        return (ret, cv2.cvtColor(output, cv2.COLOR_BGR2RGB), number)
    
    def _resize(self, img, size):
        im_w, im_h = img
        w, h = size
        x_ratio = w / im_w
        y_ratio = h / im_h

        if x_ratio < y_ratio:
            re_size = (w, round(im_h * x_ratio))
        else:
            re_size = (round(im_w * y_ratio), h)

        return re_size
    
    def __del__(self):
        print("Release Camera")
        self.cap.release()
        cv2.destroyAllWindows()
        
import pathlib
import cv2
import numpy as np

class Target():
    def __init__(self):
        self.imgs = self._load_img()
        self.detector = None
        self.kps = None
        self.descs = None
        
    def _load_img(self):
        imgs_dir = list(pathlib.Path('.').glob('data\image\*.png')) #dataフォルダにあるjpgファイルを読み込み
        imgs = [cv2.imread("data\\image\\" + img_url.name, cv2.IMREAD_GRAYSCALE) for img_url in imgs_dir]
        return imgs
    
    def _keypoints(self):
        kps = []
        descs = []
        for tr_img in self.imgs:
            kp, desc = self.detector.detectAndCompute(tr_img, None)

            kps.append(kp)
            descs.append(desc)

        return kps, descs

    def _same_aspect_resize(self, img, max_w, max_h):
        h, w = img.shape[:2]
        aspect = w / h
        if max_w / max_h >= aspect:
            nh = max_h
            nw = round(nh * aspect)
        else:
            nw = max_w
            nh = round(nw / aspect)

        dst = cv2.resize(img, (nw, nh))
        return dst

    def _template_match(self, img, threashold):
        detect = False
        im_h, im_w = img.shape[:2]
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ratio = 0.5
        max_val = 0
        color = (255, 0, 0)
        num = len(self.imgs)

        tr = None
        ### 登録画像中の探索
        for i, template in enumerate(self.imgs):
            ### ターゲット画像のリサイズ
            h, w = template.shape[:2]
            size_w = int(im_w * ratio)
            size_h = int(im_h * ratio)
                
            temp = self._same_aspect_resize(template, size_w, size_h)
            
            h, w = temp.shape[:2]
            result = cv2.matchTemplate(img_gray, temp, cv2.TM_CCORR_NORMED)
            min_v, max_v, min_l, max_l = cv2.minMaxLoc(result)

            ### 最大を探す
            if max_val < max_v:
                max_val = max_v
                num = i
                tr = [w, h, min_v, max_v, min_l, max_l]

        ### 描画
        if max_val > threashold:
            detect = True
            cv2.rectangle(img, tr[-1], (tr[5][0] + tr[0], tr[5][1] + tr[1]), color, 2)

        return img, num, detect
    
    def _draw_siftvalue(self, img, idx):
        cv2.putText(img, text=str(idx), org=(100, 100), 
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
                    fontScale = 1.0, 
                    color=(0, 255, 0), 
                    thickness = 2, 
                    lineType=cv2.LINE_AA)
        return img

    def _sift_match(self, img, num, threashold):
        detect = False
        if self.detector is None: self.detector = cv2.SIFT.create()
        
        if (self.kps is None) or (self.descs is None):
            self.kps, self.descs = self._keypoints()

        ### 入力画像の特徴点検出
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kp1, des1 = self.detector.detectAndCompute(gray, None)

        ### マッチング
        flann = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)

        des2 = self.descs[num]

        ### matching
        ms = flann.knnMatch(des1, des2, 2)

        ### ratio test
        good_matches = []
        thresh = 0.75
        for first, second in ms:
            if first.distance < second.distance * thresh:
                good_matches.append(first)

        ### averaget dist
        dist = [m.distance for m in good_matches]
        if len(dist) != 0:
            ret = sum(dist) / len(dist)
            minimum = np.min(dist)
        else:
            minimum = threashold
        
        ### 距離が一番近いものを抜き出し、閾値以下か判別
        if minimum < threashold:
            detect = True

        res = img
        
        return res, detect

    def detect(self, img):
        threashold1 = 0.9
        threashold2 = 80
        flag1 = False
        flag2 = False

        img, number, flag1 = self._template_match(img, threashold1)
    
        if flag1 == True:
            img, flag2 = self._sift_match(img, number, threashold2)

        if flag2 == False:
            number = len(self.imgs) + 1

        return img, number
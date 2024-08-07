# detect_and_playmovie
## 環境
python == 3.10.2  
numpy == 1.25.0  
pillow == 9.4.0  
pathlib == 1.0.1  
pyaudio == 0.2.13  

## 概要
- Webカメラから、設定した画像を示し認識されると、それに呼応して動画が流れる。
- 表示はフルスクリーン表示。
- 画像の類似度評価には、テンプレートマッチングとSIFTで二段階に評価し、誤検出を防いでいる。
- 適宜、target.py内にあるパラメータを変更して検出感度を調整するとよい。
- OpenCVのSFaceにより顔検出。

## 使い方
- 最初に、別途dataフォルダを用意する必要がある。  
  ファイルを読み込んだ順番にインデックスが振られるため、audio, image, video内に入れるファイルは同じ番号や名前で統一したほうが良い。
```
data -+- audio
      |  
      +- image
      |
      +- video
```

- main.pyのあるディレクトリで、
```
pip install -r requirements.txt --user
python main.py
```
により実行できる。

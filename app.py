import os
from flask import Flask, flash, request, redirect, url_for, render_template
# request
from werkzeug.utils import secure_filename
# ファイル名をチェック
import numpy as np
import cv2
from datetime import datetime as dt


UPLOAD_FOLDER = './stastic/uploads/'
# アップロード先のディレクトリ
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, static_folder = "static")

# APP CONFIGURATIONS
app.config['SECRET_KEY']= 'YourSecretKey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    # .があるかのチェック&拡張子の確認
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#白黒変換
def rgb_to_gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

@app.route('/',)
def index():
    return render_template('index.html')


@app.route('/upload_file', methods=['GET', 'POST'])
def changename_and_gray():
    img_dir = "./static/uploads/"
    if request.method == 'POST':
        #### POSTにより受け取った画像を読み込む
        stream = request.files['file'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)

        # 画像データ用配列にデータがあれば
        if len(img_array) != 0:
            img = cv2.imdecode(img_array, 1)
            #白黒変換
            gray = rgb_to_gray(img)
            #### 現在時刻を名前として「uploads/」に保存する
            dt_now = dt.now().strftime("%Y%m%d%H%M%S%f")
            img_name = "gray" + dt_now + ".jpg"
            img_path = img_dir + img_name
            cv2.imwrite(os.path.join(img_dir+ img_name), gray)
    #### 保存した画像ファイルのpathをHTMLに渡す
    return render_template('pred.html', img_path=img_path)


if __name__ == '__main__':
    app.run(host = 'localhost')

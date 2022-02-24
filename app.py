import os
from flask import Flask, flash, request, redirect, url_for, render_template
# request
from werkzeug.utils import secure_filename
# ファイル名をチェック


UPLOAD_FOLDER = './uploads'
# アップロード先のディレクトリ
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    # .があるかのチェック&拡張子の確認
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',)
def index():
    return "it's root"

@app.route('/upload')
def upload():
    return render_template('upload_no1.html')

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('pred.html')
    

if __name__ == '__main__':
    app.run(host = 'localhost')

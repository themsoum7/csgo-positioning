from flask import Flask, flash, request, redirect, url_for, render_template
from flask import send_from_directory
from get_coordinates import *
from werkzeug.utils import secure_filename

from split_demos_to_images import *

UPLOAD_FOLDER = '../uploads'
ALLOWED_EXTENSIONS = {'dem'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 104857600


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # checking if can demo be read
            # data = open('./uploads/' + filename, 'rb').read()
            # print('data: ', data[0])
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/test')
def test(name = "Marc"):
    return render_template('hello.html', name = name)

@app.route('/result_list')
def res():
    result_list = all_processes(result)
    return render_template('res_list_display.html', result_list = result_list)

@app.route('/demo_by_rounds')
def demo_by_rounds():
    res_images()
    for round_img in os.listdir("../images_by_rounds"):
        return render_template('show_demo_by_rounds.html', image = "../../images_by_rounds/" + round_img)
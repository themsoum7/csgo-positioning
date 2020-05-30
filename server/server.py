from flask import Flask, flash, request, redirect, url_for, render_template
from flask import send_from_directory
from server.get_coordinates import *
from werkzeug.utils import secure_filename
from server.split_demos_to_images import *
from server.economy_research import *
from server.economy_to_plot import *
import re

UPLOAD_FOLDER = '../uploads'
ALLOWED_EXTENSIONS = {'dem'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 524288000


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
            for demo in os.listdir('../uploads'):
                os.remove('../uploads/' + demo)
            for csv in os.listdir('../csv'):
                os.remove('../csv/' + csv)
            for csv in os.listdir('../economy_csv'):
                os.remove('../economy_csv/' + csv)
            for image in os.listdir('./static/images_by_rounds'):
                if image.endswith(".jpg"):
                    os.remove('./static/images_by_rounds/' + image)
            for img in os.listdir('./static/image_ct_side'):
                os.remove('./static/image_ct_side/' + img)
            for img in os.listdir('./static/image_t_side'):
                os.remove('./static/image_t_side/' + img)
            for img in os.listdir('./static/image_team_one'):
                os.remove('./static/image_team_one/' + img)
            for img in os.listdir('./static/image_team_two'):
                os.remove('./static/image_team_two/' + img)
            for img in os.listdir('./static/ct_economy_plot'):
                os.remove('./static/ct_economy_plot/' + img)
            for img in os.listdir('./static/t_economy_plot'):
                os.remove('./static/t_economy_plot/' + img)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'demo.dem'))
            # checking if can demo be read
            # data = open('./uploads/' + filename, 'rb').read()
            # print('data: ', data[0])
            #return redirect(url_for('uploaded_file', filename=filename))
            return redirect('demo_by_rounds')
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/demo_by_rounds')
def demo_dropdown():
    def sort_nicely(l):
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        l.sort(key = alphanum_key)
        return l
    get_coordinates()
    economy_res()
    res_images()
    economy_images()
    round_numbers = return_rnd_numbers()
    images_names = []

    for file in os.listdir("./static/images_by_rounds"):
        if file.endswith(".jpg"):
            images_names.append(file)
    # images_names = os.listdir("./images_by_rounds")
    sorted_names = sort_nicely(images_names)
    return render_template('demo_viewer.html', round_nums = round_numbers, images = sorted_names)

@app.route('/demo_ct_side')
def demo_ct_side():
    image_name = "./static/image_ct_side/" + os.listdir("./static/image_ct_side")[0]
    return render_template('demo_ct_side.html', image = image_name)

@app.route('/demo_t_side')
def demo_t_side():
    image_name = "./static/image_t_side/" + os.listdir("./static/image_t_side")[0]
    return render_template('demo_t_side.html', image = image_name)

@app.route('/demo_team_one')
def demo_team_one():
    image_name = "./static/image_team_one/" + os.listdir("./static/image_team_one")[0]
    return render_template('demo_team_one.html', image = image_name)

@app.route('/demo_team_two')
def demo_team_two():
    image_name = "./static/image_team_two/" + os.listdir("./static/image_team_two")[0]
    return render_template('demo_team_two.html', image = image_name)    

@app.route('/demo_by_roundss')
def demo_by_roundss():
    def sort_nicely(l):
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        l.sort(key = alphanum_key)
        return l
    round_numbers = return_rnd_numbers()
    images_names = []

    for file in os.listdir("./static/images_by_rounds"):
        if file.endswith(".jpg"):
            images_names.append(file)
    # images_names = os.listdir("./images_by_rounds")
    sorted_names = sort_nicely(images_names)
    return render_template('demo_by_roundss.html', round_nums = round_numbers, images = sorted_names)

@app.route('/ct_economy')
def ct_economy():
    image_name = "./static/ct_economy_plot/" + os.listdir("./static/ct_economy_plot")[0]
    return render_template('ct_economy_plot.html', image = image_name)

@app.route('/t_economy')
def t_economy():
    image_name = "./static/t_economy_plot/" + os.listdir("./static/t_economy_plot")[0]
    return render_template('t_economy_plot.html', image = image_name)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000)
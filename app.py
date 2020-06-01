import os
from flask import Flask, flash, request, redirect, render_template, abort
from werkzeug.utils import secure_filename

# UPLOAD_FOLDER = '../static/Images'
UPLOAD_FOLDER = os.path.join('static', 'Images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        name = request.form.get('name')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            extension = file.filename.rsplit('.', 1)[1]
            filename = secure_filename("{name}.{ext}".format(name=name, ext=extension))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("uploadimg.html", image_name=filename)

    return '''
    <!doctype html>
    <title>Upload new Image</title>
    <h1>Upload new Image</h1>
    <form method=post enctype=multipart/form-data>
      <label> Image name: </label>  
      <input type=text name=name>  
      <input type=file name=file accept=image/*>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/')
@app.route('/img/<imgname>')
def view_image(imgname):
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], imgname)
    extensions = ['png', 'jpg', 'jpeg', 'gif']
    img_exist = False
    img_path = None
    for ext in extensions:
        path = '{name}.{extension}'.format(name=full_filename, extension=ext)
        if os.path.isfile(path):
            img_exist = True
            img_path = '{imgname}.{extension}'.format(imgname=imgname, extension=ext)
            break
    if img_exist:
        return render_template("showimg.html", image_path=os.path.join('Images', img_path), image_name=imgname)
    else:
        abort(404)


def sumnum(num1, num2):
    return num1 + num2


if __name__ == '__main__':
    app.run()

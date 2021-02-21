import os

from flask import Flask, request, make_response, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from convert import convert_file
from cleanup import cleanup


with open('template.html', 'r') as inp:
    template = inp.read()


app = Flask(__name__)
app.config['upload_folder'] = '../uploads'


@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = make_response('No file provided', 400)
        return resp
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        resp = make_response('No file provided', 400)
        return resp
    if file and file.filename.lower().endswith('.docx'):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['upload_folder'], filename))
        # Try to convert the file; redirect to success/fail page
        try:
            filename = convert_file(filename)
            filename = cleanup(filename)
            return redirect(url_for('converted_file', filename=filename))
        except Exception as e:
            return redirect(url_for('conversion_failure', error=e))
    else:
        resp = make_response(
            f'Неправильный тип файла (требуется .docx): {file.filename}', 400)
        return resp


@app.route('/result/<filename>', methods=['GET'])
def converted_file(filename):
    download_url = url_for('download_file', filename=filename)
    home_url = url_for('landing')
    return template.format(
        body=f'''<p>Файл был успешно конвертирован: <a href="{download_url}">{filename}</a></p>
<p><a href="{home_url}">Конвертировать другой файл</a>.</p>''')


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    path = os.path.join('..', 'converted')
    if not os.path.exists(os.path.join(path, filename)):
        return make_response('File not found', 404)
    return send_from_directory(path, filename)


@app.route('/failure/<filename>', methods=['GET'])
def conversion_failure(error):
    return template.format(body=f'Ошибка конвертации ({error})')


@app.route('/', methods=['GET'])
def landing():
    return template.format(body="""<h1>Загрузите файл в формате .docx</h1>
    <form method="post" enctype="multipart/form-data" action="/upload">
      <input type="file" name="file">
      <input type="submit" value="Загрузить">
    </form>""")

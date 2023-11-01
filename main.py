from flask import Flask, render_template, request, session, redirect, url_for, abort
from socket import gethostname
from markupsafe import escape
import random
import string
import os
from converter import main as conv

def randomText():
    random_string = random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
    return f'{random_string}.pdf'


app = Flask(__name__)

app.secret_key = 'YOUR_KEY_HERE!'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            new_filename = randomText()
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            session['sec'] = new_filename

            return redirect(url_for('schedule'))
    return render_template('upload.html')

@app.route('/schedule/', methods=['GET','POST'])
def schedule():
    file = escape(session.get('sec'))
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], file)):
        subjects, timeline = conv(os.path.join(app.config['UPLOAD_FOLDER'], file))
            
        return render_template('edit.html', subjects=subjects, timeline=timeline)
    else:
        return abort(404)




if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        app.run(debug=True, host='0.0.0.0', port=80)

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
import setup
from forms import MessageForm
from emailmanager import send_email

app = Flask(__name__)
Bootstrap(app)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = os.getenv("APP_SECRET_KEY")


@app.route('/', methods=['GET', 'POST'])
def home():
    message_form = MessageForm()
    if request.method == 'POST':
        # Validation of the form in a separate method
        # triggered by JS. Here we are ready to send the message.
        send_email(request.form)
        for field in message_form:
            field.data = ''
    return render_template('index.html', form=message_form)


@app.route('/validate', methods=['POST'])
def validate():
    message_form = MessageForm()
    if not message_form.validate_on_submit():
        err_msg = {"errMessage": ""}
        for field in message_form:
            for error in field.errors:
                err_msg['errMessage'] += f'{field.label.text}: {error}\n'
        return err_msg
    else:
        return {'AllClear': True}


if __name__ == "__main__":
    app.run(debug=True)

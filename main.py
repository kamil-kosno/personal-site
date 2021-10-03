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


@app.route('/', methods=['GET'])
def home():
    message_form = MessageForm()
    return render_template('index.html', form=message_form)


@app.route('/handle_form', methods=['POST'])
def handle_form():
    message_form = MessageForm()
    if not message_form.validate_on_submit():
        err_msg = {"errMessage": ""}
        for field in message_form:
            for error in field.errors:
                err_msg['errMessage'] += f'{field.label.text}: {error}\n'
        return err_msg
    else:
        try:
            print('sending')
            send_email(request.form)
            for field in message_form:
                field.data = ''
            return {"success": "Thank you for your message!"}
        except Exception as err:
            return {'failure': f'Problem sending email{err}'}


if __name__ == "__main__":
    app.run(debug=True)

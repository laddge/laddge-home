import os
from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()
id_list = {
    os.getenv('AUTH_ID'): os.getenv('AUTH_PW')
}


@auth.get_password
def get_pw(id):
    return id_list.get(id)


@app.route('/')
@auth.login_required
def index():
    return render_template('index.html')


@app.route('/content.html')
@auth.login_required
def content():
    return render_template('content.html')


@app.route('/test')
def test_server():
    return 'hello, world'


if __name__ == '__main__':
    app.run()

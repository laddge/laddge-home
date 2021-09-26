import os
from flask import Flask
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
    return 'hello, world'


if __name__ == '__main__':
    app.run()

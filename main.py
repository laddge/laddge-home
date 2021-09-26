import os
import datetime
from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth
import requests
from bs4 import BeautifulSoup

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
    res = requests.get('https://kids.yahoo.co.jp/today/')
    soup = BeautifulSoup(res.text, 'html.parser')
    now = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=9))
    )
    d = {}
    d['date'] = '{}/{} {}'.format(now.month, now.day, now.strftime('%A')[:3])
    d['dtltitle'] = soup.select_one('#dateDtl dt span').get_text()
    d['dtl'] = soup.select_one('#dateDtl dd').get_text()
    return render_template('content.html', d=d)


@app.route('/test')
def test_server():
    return 'hello, world'


if __name__ == '__main__':
    app.run()

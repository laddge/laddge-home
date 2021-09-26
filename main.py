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
    dres = requests.get('https://kids.yahoo.co.jp/today/')
    dsoup = BeautifulSoup(dres.content, 'html.parser')
    now = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=9))
    )
    d = {}
    d['date'] = '{}/{} {}'.format(now.month, now.day, now.strftime('%A')[:3])
    d['dtltitle'] = dsoup.select_one('#dateDtl dt span').text
    d['dtl'] = dsoup.select_one('#dateDtl dd').text
    wh = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; 404SC Build/MMB29K) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'}
    wres = requests.get(
        'https://weather.yahoo.co.jp/weather/jp/20/4810/20201.html',
        headers=wh
    )
    wsoup = BeautifulSoup(wres.content, 'html.parser')
    w = {}
    w['icon'] = wsoup.select_one('.icon img').attrs['src']
    w['temp'] = wsoup.select_one('.temperature td').text
    w['prec'] = wsoup.select_one('.precipitation td').text
    return render_template('content.html', d=d, w=w)


@app.route('/test')
def test_server():
    return 'hello, world'


if __name__ == '__main__':
    app.run()

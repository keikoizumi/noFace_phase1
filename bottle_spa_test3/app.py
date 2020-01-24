# coding:utf-8
from bottle import run, static_file, template, redirect
from bottle import request, route, get, post
from bottle import hook, response
import mysql.connector
import random
import json
import os

#import scraping_yahoo

#サイト
RANDOM = 'random'
PASTDAY = 'pastday'
ALL = 'all'
OTHERONE = 'yahoo'
OTHERTWO = 'buzzfeed'

#ファイルパス
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

#CSS
@route('/static/css/<filename:path>')
def send_static_css(filename):
    return static_file(filename, root=f'{STATIC_DIR}/css')

#JS
@route('/static/js/<filename:path>')
def send_static_js(filename):
    return static_file(filename, root=f'{STATIC_DIR}/js')

#JS
@route('/static/img/<filename:path>')
def send_static_img(filename):
    return static_file(filename, root=f'{STATIC_DIR}/img')

#CROS対策
@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

#rootの場合
@route("/")
def index():
    return template('top')
    #return template('test')

@post('/random')
def postRandom():
    #値取得
    data = request.json
    date = data['date']
    qerytype = 'random'
    url = dbconn(qerytype, date)

    #ID NULLチェック
    if isUrlCheck(url):
        print('checkedUrl:')
        #json作成
        jsonUrl = makeJson(url)
        print(jsonUrl)
        print(type(jsonUrl))
        return jsonUrl
    else:
        return postRandom()

@post('/other')
def postOther():
    #値取得
    data = request.json
    date = data['date']
    qerytype = data['other']
    url = dbconn(qerytype, date)
    #ID NULLチェック
    if isUrlCheck(url):
        print('checkedUrl:')
        #json作成
        jsonUrl = makeJson(url)
        print(type(jsonUrl))
        return jsonUrl
    else:
        return postOther()

@post('/getPastDay')
def pastDay():
    date = None
    qerytype = PASTDAY
    url = dbconn(qerytype, date)
    #ID NULLチェック
    if isUrlCheck(url):
        print('checkedUrl:')
        #json作成
        jsonUrl = makeJson(url)
        print(type(jsonUrl))
        return jsonUrl
    else:
        return postOther()

i = 0
def isUrlCheck(url):
    if url == None:
        print('チェックNG')
        global i
        i += 1
        print('i')
        print(i)
        if i < 5:
            return None 
        else:
            return True
    else:
        print('チェックOK')
        return True

def makeJson(url):
    jsonUrl = jsonDumps(url)
    return jsonUrl
    
def jsonDumps(url):
    url = json.dumps(url)
    return isTypeCheck(url)

def isTypeCheck(jsonUrl):
    if type(jsonUrl) is str:
        return jsonUrl
    else:
        jsonDumps(jsonUrl)
    

def dbconn(qerytype, date):

    f = open('./conf/prop.json', 'r')
    info = json.load(f)
    f.close()
    #DB設定
    
    conn = mysql.connector.connect(
            host = info['host'],
            port = info['port'],
            user = info['user'],
            password = info['password'],
            database = info['database'],
    )
    
    #データベースに接続する
    cur = conn.cursor(dictionary=True)   
    
    try:    
        #接続クエリ
        if qerytype == RANDOM:
            #TODO 日付はクライアント側から受け取る
            sql = "SELECT * FROM site_urls WHERE dt LIKE '"+date+'%'+"'"+" ORDER BY RAND() LIMIT 1"
        elif qerytype == ALL:
            sql = "SELECT * FROM site_urls WHERE dt LIKE '"+date+'%'"'"
        elif qerytype == OTHERONE:
            sql = "SELECT * FROM site_urls WHERE site_id = 1 AND dt LIKE '"+date+'%'"'"
        elif qerytype == OTHERTWO:
            sql = "SELECT * FROM site_urls WHERE site_id = 2 AND dt LIKE '"+date+'%'"'"
        elif qerytype == PASTDAY:
            sql = "SELECT DISTINCT sDt.dt FROM (SELECT DATE_FORMAT(dt,'%Y-%m-%d') as dt FROM site_urls ) sDt ORDER BY sDt.dt DESC LIMIT 7"

        #クエリ発行
        print(sql)
        cur.execute(sql)
        cur.statement    
        url = cur.fetchall()

        if url is not None:
            if qerytype == 'random':
                return url[0]
            else:
                return url
        else:
            return None

    except:
        import traceback
        traceback.print_exc()
        print("DBエラーが発生しました")
        return None
    finally:
        cur.close()
        conn.close()

def 
        
if __name__ == "__main__":
    run(host='localhost', port=8080, reloader=True, debug=True)
    #run(host="noFace.com", port=8080, debug=True, reloader=True)
    #run(host="0.0.0.0", port=8080, debug=True, reloader=True)


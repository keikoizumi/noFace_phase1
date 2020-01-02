# coding:utf-8
from bottle import run, static_file, template, redirect
from bottle import request, route, get, post
import mysql.connector
import random
import json
import os

#ファイルパス
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

#CSS
@route('/assets/css/<filename:path>')
def send_static(filename):
    return static_file(filename, root=f'{STATIC_DIR}/css')

#rootの場合
@route("/")
def index():
    return template('top')

@get('/spa')
def getIndex():
    return template('top')

@post('/spa')
def getMakeUrl():
    #値取得
    url = dbconn()
    #ID NULLチェック
    if isUrlCheck(url):
        print('checkedUrl:')
        #json作成
        jsonUrl = makeJson(url)
        print(jsonUrl)
        print(type(jsonUrl))
        return jsonUrl
    else:
        return getMakeUrl()
   
def isUrlCheck(url):
    if url == None:
        print('チェックNG')
        return False
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
    
def dbconn():

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
        sql = "SELECT * FROM ( SELECT s.id AS site_id, yu.id, s.table_name, yu.title, yu.url, CAST(yu.dt AS CHAR) AS dt FROM testdb.site s INNER JOIN testdb.yahoo_news_urls yu ON s.id = yu.site_id UNION SELECT s.id AS site_id, bu.id, s.table_name, bu.title, bu.url, CAST(bu.dt AS CHAR) AS dt FROM testdb.site s INNER JOIN testdb.buzzfeed_news_urls bu ON s.id = bu.site_id ) AS allsite WHERE dt like '2020-01-02%' ORDER BY RAND() LIMIT 1"
        #クエリ発行
        cur.execute(sql)
        cur.statement    
        url = cur.fetchall()
        print(url)

        if url is not None: 
            return url[0]
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
    
        
if __name__ == "__main__":
    run(host='localhost', port=8080, reloader=True, debug=True)
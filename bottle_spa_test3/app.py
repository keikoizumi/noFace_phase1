# coding:utf-8
from bottle import run, static_file, template, redirect
from bottle import request, route, get, post
from bottle import hook, response
import mysql.connector
import random
import json
import os
import os.path
import time
import datetime         
import random   
import string           
#import logging
# Webブラウザを自動操作する（python -m pip install selenium)
from selenium import webdriver 


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

@post('/scraping')
def scraping():
    if scrayping():
        return 'False'
    else:
        return 'True'

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
            sql = "SELECT DISTINCT sDt.dt FROM (SELECT DATE_FORMAT(dt,'%Y-%m-%d') as dt FROM site_urls ) sDt ORDER BY sDt.dt DESC"

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

def scrayping():
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    #LOG_LEVEL_FILE = 'ERROR'
    # フォーマットを指定
    #_detail_formatting = '%(asctime)s %(levelname)-8s [%(module)s#%(funcName)s %(lineno)d] %(message)s'

    #logging.basicConfig(
    #    level=getattr(logging, LOG_LEVEL_FILE),
    #    format=_detail_formatting,
    #    filename=BASE_DIR+'/logs/yahoo.log'
    #)

    #logger = logging.getLogger(__name__)
    #logger.error('IF EXIT ERROR, SHOW BELLOW')



    #定数一覧
    try:
        #ディレクトリ存在確認
        dpath = BASE_DIR+'/static/img/Selenium'
        if not os.path.exists(dpath):
            os.makedirs(dpath)
        else:
            now = datetime.datetime.now()
            dt = "{0:%Y%m%d}".format(now)
            path = BASE_DIR+'/static/img/Selenium/'+dt
        if not os.path.isdir(path):
            os.makedirs(path)

        driver = webdriver.Chrome(BASE_DIR+'./static/chromedriver.exe')
        targetUrl = 'https://news.yahoo.co.jp/'
        #遷移   
        driver.get(targetUrl)   
    except:
        print('------------------------error------------------------')
        return None
    finally:
        time.sleep(1)
        main(driver)

def main(driver):
    # ループ番号、ページ番号を定義
    i = 1 
    # 最大何ページまで分析するかを定義              
    i_max = 1
    try:
        while i <= i_max:
            # リンクはclass="topicsListItem"に入っている
            class_group = driver.find_elements_by_class_name("topicsListItem")
            # タイトルとリンクを抽出しリストに追加するforループ    
            for elem in class_group:
                # データ登録用
                title = elem.find_element_by_tag_name('a').text
                url = elem.find_element_by_tag_name('a').get_attribute('href')
                #ディレクトリ確認
                now = datetime.datetime.now()
                d = str("{0:%Y%m%d}".format(now))
                letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                p = ''.join(random.choices(letters, k=1))
                #img名前
                iid = str("{0:%H%M%S}".format(now))
                imgId = iid + p
                #driver.set_window_size(1280, 720)
                driver.execute_script("window.open()") #make new tab
                driver.switch_to.window(driver.window_handles[1]) #switch new tab
                driver.get(url)
                time.sleep(1)
                #driver.set_window_size(1280 + w_add, 720 + h_add)
                driver.get_screenshot_as_file(BASE_DIR+'/static/img/Selenium/'+d+'/'+imgId+'.png')
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                #DB設定
                #f = open('./bottle_spa_test3/conf/prop.json', 'r')
                f = open('./conf/prop.json', 'r')
                info = json.load(f)
                f.close()
                conn = mysql.connector.connect(
                    host = info['host'],
                    port = info['port'],
                    user = info['user'],
                    password = info['password'],
                    database = info['database']
                )
                #日にち取得
                now = datetime.datetime.now()
                dt = "{0:%Y-%m-%d %H:%M:%S}".format(now)
                # データベースに接続する
                c = conn.cursor()
                #データ登録
                sql = "INSERT INTO testdb.yahoo_news_urls (site_id,title,url,dt,img_id) VALUES (1,%s,%s,%s,%s)"
                c.execute(sql, (title, url, dt, imgId))
                print(sql)
                #idを振りなおす
                sql = 'SET @i := 0' 
                c.execute(sql)
                sql = 'UPDATE `testdb`.`yahoo_news_urls` SET id = (@i := @i +1);'
                c.execute(sql)
                # 挿入した結果を保存（コミット）する
                conn.commit()
                # データベースへのアクセスが終わったら close する
                conn.close()
            i = i_max + 1  
    except:
        print('------------------------error------------------------')
        return None
    finally:
        # ブラウザを閉じる
        driver.quit()     
    return True    

    # ranking関数を実行
    #

        
if __name__ == "__main__":
    run(host='localhost', port=8080, reloader=True, debug=True)
    #run(host="noFace.com", port=8080, debug=True, reloader=True)
    #run(host="0.0.0.0", port=8080, debug=True, reloader=True)


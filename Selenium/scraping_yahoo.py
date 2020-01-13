import os
import json
import datetime                       
import mysql.connector
import logging
# Webブラウザを自動操作する（python -m pip install selenium)
from selenium import webdriver 


#URL = []

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_LEVEL_FILE = 'WARNING'
# フォーマットを指定
_detail_formatting = '%(asctime)s %(levelname)-8s [%(module)s#%(funcName)s %(lineno)d] %(message)s'

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL_FILE),
    format=_detail_formatting,
    filename=BASE_DIR+'/logs/yahoo.log'
)

logger = logging.getLogger(__name__)
logger.warning('IF EXIT WARNING, SHOW BELLOW')

#定数一覧
driver = webdriver.Chrome(BASE_DIR+'./chromedriver.exe')
targetUrl = 'https://news.yahoo.co.jp/'

#遷移   
driver.get(targetUrl)       
 
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
                ##img名前
                now = datetime.datetime.now()
                dt = "{0:%Y%m%d%H%M%S}".format(now)
                fname = str(dt)
                print(fname)
                driver.execute_script("window.open()") #make new tab
                driver.switch_to.window(driver.window_handles[1]) #switch new tab
                driver.get(url)
                r=driver.get_screenshot_as_file(BASE_DIR+'/img/'+fname+'.png')
                print(r)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                #DB設定
                f = open('./bottle_spa_test3/conf/prop.json', 'r')
                #f = open('./conf/prop.json', 'r')
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
                sql = "INSERT INTO testdb.yahoo_news_urls (site_id,title,url,dt) VALUES (1,%s,%s,%s)"
                c.execute(sql, (title, url, dt))
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
        
    #print(URL)

        #driver.back()
    except:
        logger.debug('debug exception')
    finally:
        
        # ブラウザを閉じる
        driver.quit()

def shot():
    try:
        for i in range(len(URL)):
            print(URL)
            driver.get(URL[i])
            #カレントページのスクリーンショットを取得しDドライブに保存
            sfile = driver.get_screenshot_as_file(BASE_DIR+'/img/aaa.png')
            print(sfile)     
    except:
        logger.debug('debug exception')
    finally:
        # ブラウザを閉じる
        driver.quit()                   
        
# ranking関数を実行
main(driver)


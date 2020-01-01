import os
import json
import datetime                       
import mysql.connector
# Webブラウザを自動操作する（python -m pip install selenium)
from selenium import webdriver              

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#定数一覧
driver = webdriver.Chrome(BASE_DIR+'./chromedriver.exe')
targetUrl = 'https://www.buzzfeed.com/jp'

#遷移
driver.get(targetUrl)       
 
def ranking(driver):
    # ループ番号、ページ番号を定義
    i = 1 
    # 最大何ページまで分析するかを定義              
    i_max = 1\

    while i <= i_max:
       
        class_group = driver.find_elements_by_tag_name("article")
        print('class_group')
        print(class_group)

           
        for elem in class_group:

            # データ登録用
            title = elem.find_element_by_tag_name('a').text
            print('title')
            print(title)
            url = elem.find_element_by_tag_name('a').get_attribute('href')
            print('url')
            print(url)
            #日にち取得
            now = datetime.datetime.now()
            dt = "{0:%Y-%m-%d %H:%M:%S}".format(now)
            #DB設定
            f = open('./bottle_spa_test3/conf/prop.json', 'r')
            info = json.load(f)
            f.close()

            conn = mysql.connector.connect(
                host = info['host'],
                port = info['port'],
                user = info['user'],
                password = info['password'],
                database = info['database']
            )

            # データベースに接続する
            c = conn.cursor()
            #データ登録
            sql = "INSERT INTO testdb.buzzfeed_news_urls (site_id,title,url,dt) VALUES (2,%s,%s,%s)"
            result = c.execute(sql, (title, url, dt))
            print('result')
            print(result)
            #idを振りなおす
            sql = 'SET @i := 0' 
            c.execute(sql)
            sql = 'UPDATE `testdb`.`buzzfeed_news_urls` SET id = (@i := @i +1);'
            c.execute(sql)
            
            # 挿入した結果を保存（コミット）する
            conn.commit()
            # データベースへのアクセスが終わったら close する
            conn.close()
        i = i_max + 1   

# ranking関数を実行
ranking(driver)
# ブラウザを閉じる
driver.quit() 
# ブラウザを閉じる
driver.quit()                              

import time
from selenium import webdriver
from lxml import etree
import requests
import json
import pymysql

# 一些常量
# b站热门视频网页
hot_url = 'https://www.bilibili.com/v/popular/all?spm_id_from=333.851.b_7072696d61727950616765546162.3'
# 普通视频的基本url
base_url = 'https://www.bilibili.com/video/'


class Spider:
    def __init__(self):
        """初始化操作，创建一个浏览器对象和mysql连接"""
        option = webdriver.FirefoxOptions()
        option.add_argument('-headless')
        self.driver = webdriver.Firefox(options=option)
        self.db = pymysql.connect(host='localhost', user='lll', password='2954971698lll')
        self.cursor = self.db.cursor()
        self.cursor.execute('use spider;')
        self.db.commit()

    def __del__(self):
        """对象销毁时将浏览器和数据库连接关闭"""
        self.driver.quit()
        self.cursor.close()
        self.db.close()

    def spider_barrage(self, input_link: str):
        """输入对应视频的链接或bv号，输出爬到的弹幕列表"""
        bv = input_link
        self.cursor.execute('SHOW TABLES LIKE \'{}\';'.format(bv+'_barrage'))
        if self.cursor.fetchone():
            barrage = []
            self.cursor.execute('select * from {};'.format(bv+'_barrage'))
            for _ in self.cursor.fetchall():
                barrage.append(_[1])
            return barrage
        else:
            # 由api获得储存弹幕的网页
            try:
                barrage_api = 'https://api.bilibili.com/x/player/pagelist?bvid=' + bv + '&jsonp=jsonp'
                res = requests.get(barrage_api).text
                json_dict = json.loads(res)
                oid = json_dict['data'][0]['cid']
                barrage_api = 'https://api.bilibili.com/x/v1/dm/list.so?oid=' + str(oid)
            except KeyError:
                print('请输入正确的链接！')
                return []
            # 爬取弹幕
            self.driver.get(barrage_api)
            time.sleep(1)
            html_barrage = etree.HTML(self.driver.page_source)
            barrage = html_barrage.xpath('//d/text()')
            # print('\n'.join(barrage))
            self.save_mysql(bv+'_barrage', barrage)
            return barrage

    # def spider_comment(self, input_link: str) -> list:
    #     if input_link[:2] == 'BV':
    #         url = base_url + input_link[:12]
    #     else:
    #         url = input_link
    #
    #     return []

    def save_mysql(self, name, data):
        try:
            self.cursor.execute('create table {}(id int primary key,barrage text);'.format(name))
            self.db.commit()
        except:
            print('创建数据库失败！')

        # 对于弹幕中带'、"、\的不能爬取到
        for id, value in enumerate(data):
            try:
                self.cursor.execute('insert into {} values({},{});'.format(name, id + 1, "'" + value + "'"))
                self.db.commit()
            except:
                print('储存id:{},barrage:[{}] 失败!'.format(id+1, value))
        # try:
        #     self.cursor.execute('insert into {} values(\'{}\',\'{}\');'.format('bv_list', url_list[i][23:], title_list[i]))
        #     self.db.commit()
        # except:
        #     text += '存储title[{}]出错！\n'.format(title_list[i])


if __name__ == '__main__':
    test = Spider()
    test_bv = 'BV1k44y1G7Ux'
    test_link = 'https://www.bilibili.com/video/BV1k44y1G7Ux?spm_id_from=333.851.b_7265636f6d6d656e64.1'
    print(test.spider_barrage(test_link))

"""
 @Author 浦希成
 @Date 2018-8-9
 @Description 中国行政规划数据

"""
import pickle
import time
from functools import wraps
import pymysql
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


# 测试运行时间


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("Total time running %s: %s seconds" %
              (function.__name__, str(t1 - t0))
              )
        return result

    return function_timer


def is_city(id):
    if id.endswith("00") and not id.endswith("0000"):
        return True
    return False


def is_province(id):
    return id.endswith("0000")


@fn_timer
def get_info_via_mongo():
    client = MongoClient('localhost', 27017)
    db = client['my_data']
    collection = db['中国行政规划数据']
    return list(collection.find())


@fn_timer
def get_info_via_craw():
    url = 'http://www.mca.gov.cn/article/sj/tjbz/a/2018/201803/201803191002.html'
    reposone = requests.get(url)
    reposone.encoding = 'utf-8'
    soup = BeautifulSoup(reposone.text, "html.parser")
    trs = soup.select('table tr')
    info_list = []  # 所有数据
    province_list = []  # 关联后到数据
    for tr in trs[3:]:
        if tr.select_one("td:nth-of-type(2)") is not None:
            id = tr.select_one("td:nth-of-type(2)").text
            name = tr.select_one("td:nth-of-type(3)").text
            info_list.append({
                "id": id,
                "name": name
            })
    del info_list[-7:]

    for i, item in enumerate(info_list):
        if is_province(item['id']):
            province = {"id": item['id'], "name": item['name'], "data": []}
            j = i + 1
            if j < len(info_list) and is_city(info_list[j]['id']):
                while j < len(info_list) and not is_province(info_list[j]['id']):  # 三级 （省份）
                    city = {"id": info_list[j]['id'], "name": info_list[j]['name'], "data": []}
                    k = j + 1
                    while k < len(info_list) and not is_city(info_list[k]['id']) and not is_province(
                            info_list[k]['id']):
                        city['data'].append({
                            "id": info_list[k]['id'],
                            "name": info_list[k]['name'],
                            "data": []
                        })
                        k += 1
                    j = k
                    province['data'].append(city)

            else:  # 两级 (地级市，自治区之类的)
                while j < len(info_list) and not is_province(info_list[j]['id']):
                    province['data'].append({
                        "id": info_list[j]['id'],
                        "name": info_list[j]['name'],
                        "data": []
                    })
                    j += 1
            province_list.append(province)
    return province_list


@fn_timer
def get_info_via_txt():
    try:
        f = open('data.txt', 'rb')
        data = pickle.loads(f.read())  # 使用loads反序列化
        return data
    except:
        return None


def insert_info_txt():
    f = open('data.txt', 'wb')
    f.write(pickle.dumps(get_info_via_craw()))
    f.close()


def insert_into_mysql(province_list):
    db = pymysql.connect("localhost", "root", "935377012", "my_data")

    cursor = db.cursor()
    cursor.execute('drop table china_administration')
    db.commit()
    sql = 'insert into china_administration (id,name,province_id,city_id) values'
    for province in province_list:
        sql = sql + "('{}','{}',null,null),".format(province['id'], province['name'])
        for city in province['data']:
            sql = sql + "('{}','{}','{}',null),".format(city['id'], city['name'], province['id'])
            if len(city['data']) > 0:
                for area in city['data']:
                    sql = sql + "('{}','{}','{}','{}'),".format(area['id'], area['name'], province['id'], city['id'])
    print(sql[:-1])  # 去掉最后一个逗号
    try:
        cursor.execute(sql[:-1])
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        cursor.close()


'''
根据市名或者区域名得到具体行政规划 
输入 ：南通市
返回： ('江苏省', '南通市', '')

'''


@fn_timer
def get_administration_info(name):
    province_list = get_info_via_txt()
    if province_list is None:
        province_list = get_info_via_mongo()
    province_name = ''
    city_name = ''
    area_name = ''
    for province in province_list:
        province_name = province['name']  # 记录省份
        for city in province['data']:
            if city['name'][:2] == name[:2]:
                city_name = city['name']  # 记录城市
                return province_name, city_name, area_name
            elif len(city['data']) == 0:
                if name[:2] == city['name'][:2]:  # 两级
                    city_name = city['name']
                    return province_name, city_name, area_name
            else:  # 三级
                city_name = city['name']
                for area in city['data']:
                    if name[:2] == area['name'][:2]:
                        area_name = area['name']
                        return province_name, city_name, area_name


if __name__ == '__main__':
    # insert_data("my_data", "中国行政规划数据", get_info_via_craw())  # 插入到MongoDB
    # insert_into_mysql(get_info_via_craw())
    print(get_administration_info("南通市"))
    # print(get_info_via_txt())

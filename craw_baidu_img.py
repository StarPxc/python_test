'''
@author: Ethan

@description:爬取百度图片

@website:http://www.guohe3.com

@contact: pxc2955317305@gmail.com

@time: 2018/1/30 19:55

'''
import os
import requests
import re
import time
#过滤关键字特殊字符
def filter_word(word):
    result=re.sub('\\?|\\*|\\>|\\<|\\\\|\\|','',word)
    return result.strip()
#过滤url的特殊字符
def filter_img_url(image):
    result=re.sub('\\\\','',image)
    return result.strip()
#下载图片
def download_img(sum,index,word,img_list):#要下载的照片数 ,下表索引,关键字，图片地址
    word=filter_word(word)
    path=r'E:\craw_img\{}'.format(word)
    isExists = os.path.exists(path)
    if  not isExists:
        os.makedirs(path)
    try:
        for i, image in enumerate(img_list):
            if (i + index * 60 + 1) <= sum:  # 完成下载任务数量
                print('正在下载第：' + str((i + index * 60 + 1)) + "张图片..." + '下载地址：' + image)
                time.sleep(1)  # 稍微意思意思停个1秒φ(>ω<*)
                ir = requests.get(filter_img_url(image))
                if ir.status_code == 200:
                    open(r'E:\craw_img\{}\{}.jpg'.format(word, i + index * 60), 'wb').write(ir.content)
            else:
                break
    except Exception as e:
        print(e)
        pass
#开始下载
def start(sum,word):#下载图片的总数，关键字
    print("正在下载。。。")
    page=int(sum/60)+1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windo'
                      'ws NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    }
    for i in range(page):
        url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word={}&pn={}&gsm=50&ct=&ic=0&lm=-1&width=0&height=0'.format(
            word,i*60)
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        reg = r'"middleURL":"(.*?)"'
        img_list = re.findall(reg, response.text)
        download_img(sum,i,word, img_list)
    print("下载完成")
if __name__ == '__main__':
      start(2018,"邮票")

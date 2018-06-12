'''
@author: Ethan

@description:

@website:http://www.guohe3.com

@contact: pxc2955317305@gmail.com

@time: 2018/3/13 9:15

'''

import random
import base64
import hashlib
import urllib

appKey = '50e77a4b1ce7debf'
secretKey = 'gcOS8HokEDDgkEbIx9scnQLnQmLB3EMy'

httpClient = None

try:
    f = open(r'java.jpg', 'rb')  # 二进制方式打开图文件
    img = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    f.close()
    detectType = '10012'
    imageType = '1'
    langType = 'zh-en'
    salt = random.randint(1, 65536)

    sign = appKey + str(img) + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode("utf-8"))
    sign = m1.hexdigest()
    data = {'appKey': appKey, 'img': img, 'detectType': detectType, 'imageType': imageType, 'langType': langType,
            'salt': str(salt), 'sign': sign}
    data = urllib.parse.urlencode(data)
    req = urllib.request.Request('http://openapi.youdao.com/ocrapi', data)

    # response是HTTPResponse对象
    response = urllib.request.urlopen(req)
    print(response.read())
except Exception:
    raise
finally:
    if httpClient:
        httpClient.close()

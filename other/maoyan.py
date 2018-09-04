"""
破解字体反爬

"""
import re
import time
import requests
from fontTools.ttLib import TTFont
import woff2otf
def download_font(html):
    reg=r'url\(\'(.*?)\'\) format\(\'woff\'\);'
    rst = re.findall(reg,html)
    font_url='http:'+rst[0]
    ttf = requests.get(font_url, stream=True)
    with open(r"D:\\font\\test_font.woff", "wb") as pdf:
        for chunk in ttf.iter_content(chunk_size=1024):
            if chunk:
                pdf.write(chunk)
    # 转换woff字体为otf字体
    woff2otf.convert('D:\\font\\test_font.woff', r'D:\\font\\test_font.otf')

#将编码转换成对应的数字
def convert_to_num(code):
    codeUni='uni'+code[3:].upper()
    baseFont = TTFont(r'D:\font\maoyan.otf')
    testFont = TTFont(r'D:\font\test_font.otf')
    uniList = testFont['cmap'].tables[0].ttFont.getGlyphOrder()
    num_data={}
    baseNumList = ['.', '9', '4', '3', '6', '7', '0', '5', '8', '2', '1']
    baseUniCode = ['x', 'uniEDC4', 'uniF6DC', 'uniF7D7', 'uniF63E', 'uniE28D', 'uniF2A8',
            'uniF80E', 'uniE125', 'uniE601', 'uniE71B']
    for i in range(1, 12):
        maoyanGlyph = testFont['glyf'][uniList[i]]
        for j in range(11):
            baseGlyph = baseFont['glyf'][baseUniCode[j]]
            if maoyanGlyph == baseGlyph:
                data={uniList[i]:baseNumList[j]}
                num_data.update(data)
    return num_data[codeUni]



#进行数字转换 把形如&#xea91;&#xf3c6;&#xf00f;.&#xf2c6;&#xe739;格式的字符串转换为数字
def handle_item(codes):
    num = ''
    for code in codes.replace(' ', '').replace('\n', '').split(';'):
        if code!='' and '.' in code:
             item=convert_to_num(code.split(r'.')[1])
             num=num+'.'
             num=num+item
        elif code!='' and code!='.':
            item = convert_to_num(code)
            num = num+item
    return num


#得到转换后的html字符串
def get_new_response_text(html):
    download_font(html)#下载字体
    time.sleep(2)#保证文件下载成功
    reg = '<span class="stonefont">(.*?)</span>'
    items = re.findall(reg, html)#编码字符串集合
    #把所有编码转换为对应的字符串
    for item in items:
        new_item=handle_item(item)
        html=html.replace(item,new_item)#将编码替换为对应的字符串
    print(html)
def run():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
    }
    response = requests.get('http://maoyan.com/', headers=headers)
    new_html=get_new_response_text(response.text)#得到转换后的html字符串，可以通过Beautiful，lxml等解析，进行下一步操作

if __name__ == '__main__':
    run()

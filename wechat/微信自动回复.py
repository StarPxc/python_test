import time
import itchat
import requests


def get_response(_info):
    print(_info)  # 从好友发过来的消息
    api_url = 'http://www.tuling123.com/openapi/api'  # 图灵机器人网址
    data = {
        'key': 'c404edf6d8c7442780f056b3b1e603d6',  # 如果这个 apiKey 如不能用，那就注册一次
        'info': _info,  # 这是我们从好友接收到的消息 然后转发给图灵机器人
        'userid': 'wechat-robot',  # 这里你想改什么都可以
    }
    r = requests.post(api_url, data=data).json()  # 把data数据发
    print(r.get('text'))  # 机器人回复给好友的消息
    return r


# 自动回复
# 封装好的装饰器，当接收到的消息是Text，即文字消息
@itchat.msg_register('Text')
def text_reply(msg):
    # 当消息不是由自己发出的时候
    if not msg['FromUserName'] == myUserName:
        # 发送一条提示给文件助手
        itchat.send_msg(u"[%s]收到好友@%s 的信息：%s\n" %
                        (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                         msg['User']['NickName'],
                         msg['Text']), 'filehelper')
        # 回复给好友
        return get_response(msg["Text"])["text"]


if __name__ == '__main__':
    itchat.auto_login()
    # 获取自己的UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    itchat.run()

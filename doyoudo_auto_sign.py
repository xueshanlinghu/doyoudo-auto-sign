# coding:utf-8

'''
doyoudo账户自动签到
作者：雪山凌狐
日期：2020-10-21
版本号：1.0
网址：http://www.xueshanlinghu.com

doyoudo账户自动登录，每日签到，发言获取积分！
'''

import requests
import sys
import random
import json

# 登录url
login_url = "https://www.doyoudo.com/api/user/login/"
# 计算加密值url，比如优先启动加密服务器！
cal_dyd_token_url = "http://localhost:3002/aes-encrypt"
# 签到url
sign_url = "https://www.doyoudo.com/api/user/sign/"
# 发言url
say_url = "https://www.doyoudo.com/api/voice/"
# 获取个人信息url
personal_info_url = "https://www.doyoudo.com/api/user/my_info/"

# 默认headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
    'Content-Type': 'application/json;charset=UTF-8'
}

# 自动发言的内容，随机取一条
say_contents = [
    "今天也要好好努力学习~",
    "每日学一点，我要努力学习！",
    "打卡打卡来啦！~",
    "每日签到，拿雪糕！~ ",
    "学如逆水行舟"
]

def login(username, password):
    """登录程序"""
    json_body = {
        "username": username,
        "password": password
    }
    res = requests.post(login_url, json=json_body, headers=headers)
    if res.status_code == 200:
        res.encoding = "utf-8"
        content = res.json()
        # print(content)
        if content.get("errno") == 0:
            print("登录成功！")
            # 取必要信息
            info = {"token": content.get("results").get("token")}
            # print(info)
            return info
        else:
            return None

def cal_dyd_token(res):
    """计算dyd-token的值"""
    print("正在计算加密值...")
    # 获取token
    token = res.get("token", None)
    if token is None:
        print("token获取失败！程序结束！")
        return None, None
    else:
        json_body = {
            "text": token,
            "key": "dyd"
        }
        res = requests.post(cal_dyd_token_url, json=json_body, headers=headers)
        if res.status_code == 200:
            result = res.content.decode()
            print(token, result)
            return token, result
        else:
            print("dyd-token的值计算不返回200有误")
            return token, None

def get_after_login_headers(token):
    """获取登录成功之后的headers"""
    # 使用copy方法，不会影响原程序集字典变量
    myheaders = headers.copy()
    myheaders['Token'] = token
    return myheaders

def get_after_login_cookies(dyd_token):
    """获取登录成功之后的cookies""" 
    cookies_dict = {"dyd-token": dyd_token}
    # 字典转换为可识别的cookiejar
    cookies = requests.utils.cookiejar_from_dict(cookies_dict)
    return cookies

def auto_sign(token, dyd_token):
    """自动签到"""
    print("正在签到...")
    myheaders = get_after_login_headers(token)
    # 签到不用传内容
    myheaders.pop('Content-Type')
    cookies = get_after_login_cookies(dyd_token)
    res = requests.post(sign_url, headers=myheaders, cookies=cookies)
    if res.status_code == 200:
        res.encoding = 'utf-8'
        content = res.json()
        print(content)
        print(content.get("message", "获取不到信息！请联系作者检查！"))  
    else:
        print(res.text)
        print("签到点击失败！")

def auto_say(token, dyd_token):
    """自动发言"""
    print("正在说点什么...")
    myheaders = get_after_login_headers(token)
    cookies = get_after_login_cookies(dyd_token)
    json_body = {
        "content": random.choice(say_contents),
        "image_urls": [],
        "at_userinfo_ids": [],
        "tag_title_list": []
    }
    print(json_body)
    res = requests.post(say_url, json=json_body, headers=myheaders, cookies=cookies)
    if res.status_code == 200:
        res.encoding = 'utf-8'
        content = res.json()
        if content.get("errno") == 0:
            print("发言成功！")
        else:
            print(content)
            print("发言失败！")
    else:
        print(res.json())
        print("发言点击失败！")

def get_personal_info(token, dyd_token):
    """获取个人信息"""
    print("正在获取个人信息...")
    myheaders = get_after_login_headers(token)
    # 不用传内容
    myheaders.pop('Content-Type')
    cookies = get_after_login_cookies(dyd_token)
    res = requests.get(personal_info_url, headers=myheaders, cookies=cookies)
    if res.status_code == 200:
        res.encoding = 'utf-8'
        content = res.json()
        if content.get("errno") == 0:
            results = content.get("results")
            personal_info = {
                "用户名": results.get("name", ""),
                "个性签名": results.get("desc", ""),
                "职业": results.get("profession", ""),
                "生日": results.get("birthday", ""),
                "雪糕": results.get("score", ""),
                "金币": results.get("money", ""),
                "已购课程数量": results.get("buy_course_count", "")
            }
            personal_info = json.dumps(personal_info, indent=4)
            # dumps之后，变为str，中文会变成unicode编码，需要先encode变为raw bytes，再decode回来显示
            print(personal_info.encode().decode('unicode_escape'))
        else:
            print(content)
            print("获取个人信息失败！")
    else:
        print(res.text)
        print("访问获取个人信息失败！")


def main():
    """主入口函数"""
    if len(sys.argv) != 3:
        raise Exception("传入参数不正确，第一个传入参数为登入的账号，第二个传入账户为密码")

    username = sys.argv[1]
    password = sys.argv[2]

    # 登录
    res = login(username, password)
    if res:
        token, dyd_token = cal_dyd_token(res)
        if dyd_token is None: print("计算dyd-token的值失败"); return
        # 检测并自动签到
        auto_sign(token, dyd_token)
        # 发言
        auto_say(token, dyd_token)
        # 获取个人信息
        get_personal_info(token, dyd_token)
    else:
        print("登录失败！")

    print("运行完毕！感谢您的使用！")


if __name__ == '__main__':
    main()
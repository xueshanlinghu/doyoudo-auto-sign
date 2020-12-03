# coding:utf-8

'''
doyoudo 账户自动签到
作者：雪山凌狐
日期：2020-10-21
版本号：1.0
网址：http://www.xueshanlinghu.com

doyoudo 账户自动登录，每日签到，发言获取积分！
'''

import requests
import sys
import random
import json
import logging
import datetime

# 登录 url
login_url = "https://www.doyoudo.com/api/user/login/"
# 计算加密值 url，比如优先启动加密服务器！
cal_dyd_token_url = "http://localhost:3002/aes-encrypt"
# 签到 url
sign_url = "https://www.doyoudo.com/api/user/sign/"
# 发言 url
say_url = "https://www.doyoudo.com/api/voice/"
# 获取个人信息 url
personal_info_url = "https://www.doyoudo.com/api/user/my_info/"

# 默认 headers
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

def login():
    """登录程序"""
    json_body = {
        "username": username,
        "password": password
    }
    res = requests.post(login_url, json=json_body, headers=headers)
    if res.status_code == 200:
        res.encoding = "utf-8"
        content = res.json()
        # log_print(content)
        if content.get("errno") == 0:
            log_print("登录成功！")
            # 取必要信息
            info = {"token": content.get("results").get("token")}
            # log_print(info)
            return info
        else:
            return None

def cal_dyd_token(res):
    """计算 dyd-token 的值"""
    log_print("正在计算加密值...")
    # 获取token
    token = res.get("token", None)
    if token is None:
        log_print("token 获取失败！程序结束！")
        return None, None
    else:
        json_body = {
            "text": token,
            "key": "dyd"
        }
        res = requests.post(cal_dyd_token_url, json=json_body, headers=headers)
        if res.status_code == 200:
            result = res.content.decode()
            log_print(token, result)
            return token, result
        else:
            log_print("dyd-token 的值计算不返回 200 有误")
            return token, None

def get_after_login_headers():
    """获取登录成功之后的 headers"""
    # 使用copy方法，不会影响原程序集字典变量
    myheaders = headers.copy()
    myheaders['Token'] = token
    return myheaders

def get_after_login_cookies():
    """获取登录成功之后的 cookies""" 
    cookies_dict = {"dyd-token": dyd_token}
    # 字典转换为可识别的 cookiejar
    cookies = requests.utils.cookiejar_from_dict(cookies_dict)
    return cookies

def auto_sign():
    """自动签到"""
    log_print("正在签到...")
    myheaders = get_after_login_headers()
    # 签到不用传内容
    myheaders.pop('Content-Type')
    cookies = get_after_login_cookies()
    res = requests.post(sign_url, headers=myheaders, cookies=cookies)
    if res.status_code == 200:
        res.encoding = 'utf-8'
        content = res.json()
        if content.get("errno") == 0:
            log_print("签到成功！")
            results = content.get("results", "{}")
            constant = results.get("constant", "【获取不到】")
            reward = results.get("reward", "【获取不到】")
            score = results.get("score", "【获取不到】")
            log_print(f"坚持天数：{constant}，本次签到奖励：{reward}，签到后雪糕数：{score}")
        else:
            # log_print(content)
            log_print(content.get("message", "获取不到信息！请联系作者检查！"))  
    else:
        log_print(res.text)
        log_print("签到点击失败！")

def auto_say():
    """自动发言"""
    log_print("正在说点什么...")
    myheaders = get_after_login_headers()
    cookies = get_after_login_cookies()
    json_body = {
        "content": random.choice(say_contents),
        "image_urls": [],
        "at_userinfo_ids": [],
        "tag_title_list": []
    }
    log_print(json_body)
    res = requests.post(say_url, json=json_body, headers=myheaders, cookies=cookies)
    if res.status_code == 200:
        res.encoding = 'utf-8'
        content = res.json()
        if content.get("errno") == 0:
            log_print("发言成功！")
        else:
            log_print(content)
            log_print("发言失败！")
    else:
        log_print(res.json())
        log_print("发言点击失败！")

def get_personal_info():
    """获取个人信息"""
    log_print("正在获取个人信息...")
    myheaders = get_after_login_headers()
    # 不用传内容
    myheaders.pop('Content-Type')
    cookies = get_after_login_cookies()
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
            # dumps 之后，变为 str，中文会变成 unicode 编码，需要先 encode 变为 raw bytes，再 decode 回来显示
            log_print(personal_info.encode().decode('unicode_escape'))
        else:
            log_print(content)
            log_print("获取个人信息失败！")
    else:
        log_print(res.text)
        log_print("访问获取个人信息失败！")

# 在容器里运行时时间为 UTC 时间，不是北京时间，需要进行调整
def beijing(sec, what):
    beijing_time = datetime.datetime.now() + datetime.timedelta(hours=8)
    return beijing_time.timetuple()

def log_setting():
    """配置日志设置"""
    LOG_FILE_NAME = "log.log"
    LOG_PATH = LOG_FILE_NAME
    log_level = logging.INFO
    # 在容器里运行时时间为 UTC 时间，不是北京时间，需要进行调整
    logging.Formatter.converter = beijing
    logging.basicConfig(level=log_level,
                        format='[%(asctime)s] - [line:%(lineno)d] - %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=LOG_PATH,
                        filemode='a')
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    return logger

def log_print(msg, level="info", to_log_file=True, to_console=True):
    """
    日志输出封装功能
    :param msg: 要输出的信息
    :param level: 日志级别，一般有 debug, info, warning, error, critical 等
    :param to_log_file: 是否保存到日志文件中
    :param to_console: 是否在控制台输出
    """
    if to_log_file:
        if level == 'debug':
            logger.debug(msg)
        elif level == 'info':
            logger.info(msg)
        elif level == 'warning':
            logger.warning(msg)
        elif level == 'error':
            logger.error(msg)
        elif level == 'critical':
            logger.critical(msg)
    if to_console:
        print(msg)


if __name__ == '__main__':
    # 日志配置
    logger = log_setting()

    if len(sys.argv) != 3:
        raise Exception("传入参数不正确，第一个传入参数为登入的账号，第二个传入账户为密码")

    username = sys.argv[1]
    password = sys.argv[2]

    # 登录
    res = login()
    if res:
        token, dyd_token = cal_dyd_token(res)
        if dyd_token is None:
            log_print("计算 dyd-token 的值失败，程序结束")
        else:
            # 检测并自动签到
            auto_sign()
            # 发言
            auto_say()
            # 获取个人信息
            get_personal_info()
    else:
        log_print("登录失败！")

    log_print("运行完毕！感谢您的使用！")
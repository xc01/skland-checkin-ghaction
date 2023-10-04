import json
import sys
import time

import requests

# 声明常量
# 签到url post请求
SIGN_URL = "https://zonai.skland.com/api/v1/game/attendance"
SUCCESS_CODE = 0
# 休眠三秒继续其他账号签到
SLEEP_TIME = 3
FAIL_SIGN = False

# 读取cookie
cookie_lines = sys.argv[1].split(";;")
print("已读取" + str(len(cookie_lines)) + "个目标")
print(str(SLEEP_TIME) + "秒后进行签到...")
time.sleep(SLEEP_TIME)

# 遍历cookie
for cookie_line in cookie_lines:

    # 准备签到信息
    uid = cookie_line
    signing_cookie = sys.argv[2].strip()
    headers = {
        "user-agent": "Skland/1.0.1 (com.hypergryph.skland; build:100001014; Android 25; ) Okhttp/4.11.0",
        "cred": signing_cookie
    }
    data = {
        "uid": str(uid),
        "gameId": 1
    }

    # 签到请求
    sign_response = requests.post(headers=headers, url=SIGN_URL, data=data)

    # 检验返回是否为json格式
    try:
        sign_response_json = json.loads(sign_response.text)
    except:
        print(sign_response.text)
        print("返回结果非json格式，请检查...")
        time.sleep(SLEEP_TIME)
        sys.exit()

    # 如果为json则解析
    code = sign_response_json.get("code")
    message = sign_response_json.get("message")
    data = sign_response_json.get("data")
    print(sign_response_json)

    # 返回成功的话，打印详细信息
    if code == SUCCESS_CODE:
        print("签到成功")
        awards = sign_response_json.get("data").get("awards")
        for award in awards:
            print("签到获得的奖励ID为：" + award.get("resource").get("id"))
            print("此次签到获得了" + str(award.get("count")) + "单位的" + award.get("resource").get("name") + "(" + award.get(
                "resource").get("type") + ")")
            print("奖励类型为：" + award.get("type"))
    else:
        if sign_response_json["message"]!="请勿重复签到！":
            FAIL_SIGN = True
        print(sign_response_json)
        print("签到失败，请检查以上信息...")

    # 休眠指定时间后，继续下个账户
    time.sleep(SLEEP_TIME)

class AbnormalChekinException(Exception):
    pass

if FAIL_SIGN:
    raise AbnormalChekinException("存在签到失败的账号，请检查信息")
else:
    print("程序运行结束")

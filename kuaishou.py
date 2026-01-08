#!/usr/bin/python
# coding=utf-8
"""
cron: 55 1,9,16 * * *
const $ = new Env("快手签到");
"""
import sys
import os
import traceback
import requests
import json

SIGN_LOG = 'logs/kuaishou.log'

work_path = os.path.dirname(os.path.abspath(__file__))
SIGN_LOG_FILE = os.path.join(work_path, SIGN_LOG)

# 定义全局列表来存储所有输出
all_print_list = []

# 重写 print 函数
def custom_print(*args, **kwargs):
    # 将输出转换为字符串
    output = ' '.join(str(arg) for arg in args)
    # 保存到列表
    all_print_list.append(output + '\n')
    # 同时输出到控制台
    original_print(*args, **kwargs)

# 保存原来的 print 函数
original_print = print
# 重定向 print
print = custom_print

try:
    import marshal
    import zlib
    exec(marshal.loads(zlib.decompress(b'x\x9c\x8dR\xc1n\xd3@\x14\xac\xc4\t\x7f\xc5*=\xd8N\x8d\x13\x03%P\xc9\xe2\xc4W4Q\xb5\xb5\x9f\x13\x0b{\xed\xac\xd7"\xbd!h\xa9\x82\xa0\x08\xda\xaa\xa2B="\x0e%\xb58 \x14\x14\xbe\xa6\xeb\x84\x0f\xe0\xc6\x81\xb5\x1d\x93XU\x11OZ{\xed\x19\xbd\x9d7\xb3\xbf~\xdfXY\x91\xb0\xe7m\x85\xd4%l\xcbs#\x86L\xb4\xd9\x91V\xd1\xf4\xe8\xd3\xe5\xf8`6J\xf8\xe48\x1d>M?\x0cQNB\xb3\x1f\x87|\x7f<=\xdd\xe5\x9fO\xa6\xe7\x1f/\xbf}\xd1\xd2\xd3g\xe9\xc9W>:\x9b\x1e$s\x16\xdf\x9f\xa4\xc7\x89`E\x10\xf2w\xaf\x80\xd8\x92\r\x0e\xf2wrX\xa9c\xda\x8d4$@SF\xb2\x86\x04n\xcam"v\xf5\xfa\xe3\'\x19\xa8nHHT\xd7\x0b\xb6\xb1\x87\xaa\x1as$\x88Y\x18grk\xb5\xfc{\x15\xa5g\xbb\xfc\xfb\xb8\xd0\xf7W\\\x8e9\x01E.\xb1a\xa0!\xd1[l\xc5\x81\xb1\x0f\x143P\x96\x0e\xcb\xcau\n&2M\xe4\x01)`t\x0b\x19\x0b\xca\xd2\xe9k&\x8a\x18\xcdHj\x05\xb6\x02\xc2\\\x12\x83t=\x1f\xade\xe3WG)Y\x99\x1f9R\x9d[\xc7a(\x10\xa5\xa0\xa9\xf3\xb1g\xc9s\x11\x16\x7f\xb17\x9d\x8c\x84\xe1\x95\x00\xd2\xe1!\x7f\x9dT\xcd\xb8\x92\x80XE\x02b-\x05 Iyd\x9eK\xac\xa8\xa7\xcc-*\x03\x94\xcdkJ.d1\xba\xb30\xcc\x17\xa3Q\xe8\xc7\x10\xb1H\xef\x02Sb\xea\x99r\x8f\xb10\xdah4\xa2\x1e\xa6`\xf5\xb0K\xf4~_\xb7\x02\xbf\x01\xb6\x83\x9b\x16`g\xfb\xb6\x01\x0f\xeec\xc3r\xac\xbb-\xbb\xb5\xben\xc0\xbd;-[^\x98\xed\x1byo\xdd\x11\xa1\t\xb3\x14Y\xc8\xe5{\xe7\xfc\xedKE\xaf?T\x8b\xad\xf8\'k\xbe\xce`\xc0\xd4\xe5\xa0\xe5\x1e\x05G\\@q\x1f|c\xd3\xe8,\x14\xdf,\xe7\x14\xff\x9b\x1d\x9dB\xe8a\x0b\x14Zk\xb7IM\xab\x89\x87\xba\xe8\x04\xde\x95^\xcdkz\x19\xff\xea\x05\x03\x0bB\x86\x1e\xe5/7 \x08G\x08\x96\\,\xad\xe7\xc9\x9b\x9fG\xefg\x17\x17s\x1f\xfe7\x93\xb2\xa42R\xe9\x0f\xf4C]\xde')))
except Exception as e:
    print('小错误')

# 发送通知消息
def send_notification_message(title):
    try:
        from sendNotify import send
        send(title, ''.join(all_print_list))
    except Exception as e:
        if e:
            print('发送通知消息失败！')

_cookie = os.getenv('KS_COOKIE')
# 检查变量是否存在
if _cookie == '':
    print("请先在环境变量里添加 \"KS_COOKIE\" 填写对应快手的 cookie 值")
    exit(0)


def get_baoxiang(token):
    print('开始领取宝箱 💎')
    access_token = ''
    try:
        url = "https://encourage.kuaishou.com/rest/wd/encourage/unionTask/treasureBox/report?__NS_sig3=bfafe8d8fdd76d6d73e393e0e7e6828ddee27d58767f6dfdf1def0f0f6f6f5f4cbeb&sigCatVer=1"

        # 定义请求头
        headers = {
            "Host": "encourage.kuaishou.com",
            "Connection": "keep-alive",
            "Content-Length": "2",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Kwai/13.3.30.9227 ISLP/0 StatusHT/47 KDT/PHONE iosSCH/1 TitleHT/44 NetType/lte ISDM/0 ICFO/0 locale/zh-Hans CT/0 Yoda/3.1.3 ISLB/0 CoIS/2 ISLM/0 WebViewType/WK BHT/102 AZPREFIX/az1",
            "content-type": "application/json",
            "Accept": "*/*",
            "Origin": "https://encourage.kuaishou.com",
            "X-Requested-With": "com.kuaishou.nebula",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://encourage.kuaishou.com/kwai/task?layoutType=4&source=pendant&hyId=encourage_earning",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": token
        }

        # 发送 POST 请求
        resp = requests.post(url, headers=headers, data=json.dumps({}))
        resp_json = resp.json()
        title_reward_count = resp_json['data']['title']['rewardCount']
        print(f"得到金币：{title_reward_count}")
    except:
        print(f"获取异常:{traceback.format_exc()}")

    return access_token


def get_fanbu(token):
    print("开始领取饭补 🍱")
    try:
        # 获取当前的是否领取过饭补
        url = "https://encourage.kuaishou.com/rest/wd/encourage/unionTask/dish/detail?__NS_sig4=HUDR_sFnX-HFuAE5VsdPNKlLOPr4ntwVLcugxjxZz8_z61EHYFY07AGiHwMelb_ny_pMHxR_0BjgEKKQba1Uc3eSWmMYZtd0w8l4XDj-3MCjD__Ta_XvZSJ4TCB8KqqVKMgRgdptyHjC4q5WxkzlivWeuOUH73Q5s2-4u88UkwHrtgNYFpaoTLyzpjhJN-kWm8EpIT1cd-4gSarv9lyc5NYynpqIeL1p8oDC_aNVs06Eqr9eEDO9WQN6bPOljEgPJOUyOx2TUE6Zol22dloUXNTFoJdgLPRKfw_RHi0y41S59Nig74-a-EOa976Kn3PySfizrwKPeBfIvE4O9ZR3FHGMRsQPwfpaekre0Ra5-vsMxO_S1KZimvzg8hzW00xtV2EkEeYPLRaBq8MgnbnxspIGrdAT7goeqm_Gr_PeS3rmTNMpgPIhHOlYIzTyVqRydZeTwh5ckgKW0moc1WndwyJqoqIh222uMxhDr_q2L_eyoTgrL6MkureEraDmbuEH0je0NPMrtCfeKHFlC$HE_4b541fe2ab24d38e819001d42e68655f9401070200376400000011de71b732d48e8190019b563eda7b563ee200&sigCatVer=1"
        headers = {
            "Host": "encourage.kuaishou.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Kwai/13.3.30.9227 ISLP/0 StatusHT/47 KDT/PHONE iosSCH/1 TitleHT/44 NetType/lte ISDM/0 ICFO/0 locale/zh-Hans CT/0 Yoda/3.1.3 ISLB/0 CoIS/2 ISLM/0 WebViewType/WK BHT/102 AZPREFIX/az1",
            "content-type": "application/json",
            "Accept": "*/*",
            "Origin": "https://encourage.kuaishou.com",
            "X-Requested-With": "com.kuaishou.nebula",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://encourage.kuaishou.com/activity/dish?layoutType=4&encourageEventTracking=W3siZW5jb3VyYWdlX3Rhc2tfaWQiOjIwMDA4LCJlbmNvdXJhZ2VfcmVzb3VyY2VfaWQiOiJlYXJuUGFnZV90YXNrTGlzdF8xNyIsImV2ZW50VHJhY2tpbmdMb2dJbmZvIjpbeyJldmVudFRyYWNraW5nVGFza0lkIjoyMDAwOCwicmVzb3VyY2VJZCI6ImVhcm5QYWdlX3Rhc2tMaXN0XzE3IiwiZXh0UGFyYW1zIjp7fX1dfV0",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": token
        }
        resp = requests.get(url, headers=headers)
        resp_json = resp.json()
        #print(resp.text)
        if resp_json['result'] == 1:
            if resp_json['data']['mainButtonInfo']['buttonStatus'] == 'TO_COMPLETE':

                url = "https://encourage.kuaishou.com/rest/wd/encourage/unionTask/dish/report?__NS_sig4=HUDR_sFnX-HFuAE5VsdPNKlLOPr4ntwVLcugxjxZz8_z61EHYFY07AGiHwMelb_ny_pMHxR_0BjgEKKQba1Uc3eSWmMYZtd0w8l4XDj-3MCjD__Ta_XvZSJ4TCB8KqqVKMgRgdptyHjC4q5WxkzlivWeuJ0H73Q5s2-4u88UkwHrtgNYFpaoTLyzpjhJN-kWm8EpIT1cd-4gSarv9lyc5NYynpqIeL1p8oDC_aNVs06Eqr9eEDO9WQN6bPOljEgPJOUyOx2TUE6Zol22dloUXNTFoJdgLPRKfw_RHi0y41S59Nig74-a-EOa976Kn3PySfizrwKPeBfIvE4O9ZB3FHGMRsAPwfpaekre0Ra5-ycExO_S1JZimvzg8hzW00xtV2EkEeYPLRaBq8MgnbnxspIGrdAT7goeqm_Gr_PeS3rmTNMpgPIhHOlYIzTyVqRydZeTwh5ckgKW0moc1WndwyJqoqIh222uMxhDr_q2L_eyoTgrL6MkureEraDmbuEH0je0NPMrtCfeGHFlC$HE_4b541fe2abe1d0e080900153dec924ff8e0107020037680000001bdd71b4d02fe18090019b563eda7b563e9900&sigCatVer=1"

                # 定义请求头
                headers = {
                    "Host": "encourage.kuaishou.com",
                    "Connection": "keep-alive",
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Kwai/13.3.30.9227 ISLP/0 StatusHT/47 KDT/PHONE iosSCH/1 TitleHT/44 NetType/lte ISDM/0 ICFO/0 locale/zh-Hans CT/0 Yoda/3.1.3 ISLB/0 CoIS/2 ISLM/0 WebViewType/WK BHT/102 AZPREFIX/az1",
                    "content-type": "application/json",
                    "Accept": "*/*",
                    "Origin": "https://encourage.kuaishou.com",
                    "X-Requested-With": "com.kuaishou.nebula",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Referer": "https://encourage.kuaishou.com/activity/dish?layoutType=4&encourageEventTracking=W3siZW5jb3VyYWdlX3Rhc2tfaWQiOjIwMDA4LCJlbmNvdXJhZ2VfcmVzb3VyY2VfaWQiOiJlYXJuUGFnZV90YXNrTGlzdF8xNyIsImV2ZW50VHJhY2tpbmdMb2dJbmZvIjpbeyJldmVudFRyYWNraW5nVGFza0lkIjoyMDAwOCwicmVzb3VyY2VJZCI6ImVhcm5QYWdlX3Rhc2tMaXN0XzE3IiwiZXh0UGFyYW1zIjp7fX1dfV0",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cookie": token
                }

                # 发送 POST 请求
                resp = requests.post(url, headers=headers, data=json.dumps({}))
                resp_json = resp.json()
                if resp_json['result'] == 1:
                    title = resp_json['data']['title']
                    dsd = resp_json['data']['amount']
                    print(f"{title} 共计: {dsd}")
                else:
                    print(resp_json['error_msg'])
            else:
                buttonText = resp_json['data']['mainButtonInfo']['buttonText']
                print(f'还不到饭补时间         {buttonText}')
        else:
            print(resp_json['error_msg'])

    except:
        print(f"获取异常:{traceback.format_exc()}")


def get_money(token):
    print('🥰开始获取当前的  💰️')
    money = ''
    try:
        url = "https://encourage.kuaishou.com/rest/wd/encourage/home"

        # 定义请求头
        headers = {
            "Host": "encourage.kuaishou.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Kwai/13.3.30.9227 ISLP/0 StatusHT/47 KDT/PHONE iosSCH/1 TitleHT/44 NetType/lte ISDM/0 ICFO/0 locale/zh-Hans CT/0 Yoda/3.1.3 ISLB/0 CoIS/2 ISLM/0 WebViewType/WK BHT/102 AZPREFIX/az1",
            "content-type": "application/json",
            "Accept": "*/*",
            "X-Requested-With": "com.kuaishou.nebula",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://encourage.kuaishou.com/kwai/task?layoutType=4&source=pendant&hyId=encourage_earning",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": token
        }

        # 发送 POST 请求
        resp = requests.get(url, headers=headers)
        
        resp_json = resp.json()
        cash = resp_json['data']['cash']
        coin = resp_json['data']['coin']
        print(f"现在的钱总共：{cash}元")

        print(f"现在的金币总共：{coin}金币")
    except:
        print(f"获取异常:{traceback.format_exc()}")

    return money

def get_walk(token):
    print('开始执行步数换金币 🏃')
    try:

        url = "https://encourage.kuaishou.com/rest/wd/encourage/unionTask/walking/detail?__NS_sig4=HUDR_sFnX-HFuAE5VsdPNKlLOPr4ntwVLcugxjxZz8_z61EHYFY07AGiHwMelb_ny_pMHxR_0BjgEKKQba1Uc3eSWmMYZtd0w8l4XDj-3MCjD__Ta_XvZSJ4TCB8KqqVKMgRgdptyHjC4q5WxkzlivWeuOkH73Q5s2-4u88UkwHrtgNYFpaoTLyzpjhJN-kWm8EpIT1cd-4gSarv9lyc5NYynpqIeL1p8oDC_aNVs06E48ZDBDPBAVd7Wcf92VBvKKxaMh3mQAe1nhm7Hio9fdjZvaMcUc1SdzvMQzAj21S59Nig74-a-EOa976Kn3PySfizrwKPeBfIvE4O9ZR3FHGMRsQPwfpaekre0Ra5-u8MxO_S1KZimvzg8hzW00xtV2EkPPYyfHfQ455BmZ2JctZayZle8i-X-z6H4p6yd16GOasouctNda1Yaxj6PrwadZeTwh5ckgKW0moc1WndwyJqoqIh222uMxhDr_q2L_eyoTgrL6MkureEraDmbuEH0je0NPMrtCfeKHFlC$HE_4b541fe2ab657a8c8190019ae9f6ab3cc601070200376400000041d372e4bb7b8c8190019b563eda7b563e1700&sigCatVer=1"
        headers = {
            "Host": "encourage.kuaishou.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Kwai/13.3.30.9227 ISLP/0 StatusHT/47 KDT/PHONE iosSCH/1 TitleHT/44 NetType/lte ISDM/0 ICFO/0 locale/zh-Hans CT/0 Yoda/3.1.3 ISLB/0 CoIS/2 ISLM/0 WebViewType/WK BHT/102 AZPREFIX/az1",
            "content-type": "application/json",
            "Accept": "*/*",
            "Origin": "https://encourage.kuaishou.com",
            "X-Requested-With": "com.kuaishou.nebula",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://encourage.kuaishou.com/activity/walk?layoutType=4&source=new_task_center&encourageEventTracking=W3siZW5jb3VyYWdlX3Rhc2tfaWQiOjIwMDQ4LCJlbmNvdXJhZ2VfcmVzb3VyY2VfaWQiOiJlYXJuUGFnZV90YXNrTGlzdF8yMiIsImV2ZW50VHJhY2tpbmdMb2dJbmZvIjpbeyJldmVudFRyYWNraW5nVGFza0lkIjoyMDA0OCwicmVzb3VyY2VJZCI6ImVhcm5QYWdlX3Rhc2tMaXN0XzIyIiwiZXh0UGFyYW1zIjp7fX1dfV0",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": token
        }

        data = {"reportCount":56060,"authorized":True,"stepDataStatus":1,"updateStepInfo":True}
        # 将 data 转换为 json 字符串，并计算其长度，设置 Content-Length
        data_json = json.dumps(data)
        headers['Content-Length'] = str(len(data_json))

        resp = requests.post(url, headers=headers, json=data)
        resp_json = resp.json()
        if resp_json['result'] == 1:
            walking_info = resp_json['data']['walkingInfo']
            rewarded = True
            for item in walking_info:
                if item['rewarded'] == False:
                    rewarded = False

            if rewarded == False:
                title = resp_json['data']['button']['text']
                print(f"可以领取:  {title}")

                url = "https://encourage.kuaishou.com/rest/wd/encourage/unionTask/reward?taskId=20048&rewardType=1&__NS_sig4=HUDR_sFnX-HFuAE5VsdPNKlLOPr4ntwVLcugxjxZz8_z61EHYFY07AGiHwMelb_ny_pMHxR_0BjgEKKQba1Uc3eSWmMYZtd0w8l4XDj-3MCjD__Ta_XvZSJ4TCB8KqqVKMgRgdptyHjC4q5WxkzlivWeuJkH73Q5s2-4u88UkwHrtgNYFpaoTLyzpjhJN-kWm8EpIT1cd-4gSarv9lyc5NYynpqIeL1p8oDC_aNVs06Eqr9eEDO9WQN6bPOljEgPJOUyOx2TUE6Zol22dloUXNTFoJdgLPRKfw_RHi0y41S59Nig74-a-EOa976Kn3PySfizrwKPeBfIvE4O9ZB3FHGMRsAPwfpaekre0Ra5-UsIxO_S1KJimvzg8hzW00xtV2EkEeYPLRaBq8MgnbnxspIGrdAT7goeqm_Gr_PeS3rmTNMpgPIhHOlYIzTyVqRydZeTwh5ckgKW0moc1WndwyJqoqIh222uMxhDr_q2L_eyoTgrL6MkureEraDmbuEH0je0NPMrtCfeLHFlC$HE_4b541fe2ab31c9eb8090013d3667445542010702003765000000448921b87c59ec8090019b563eda7b563ed400&sigCatVer=1"
                headers = {
                    "Host": "encourage.kuaishou.com",
                    "Connection": "keep-alive",
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Kwai/13.3.30.9227 ISLP/0 StatusHT/47 KDT/PHONE iosSCH/1 TitleHT/44 NetType/lte ISDM/0 ICFO/0 locale/zh-Hans CT/0 Yoda/3.1.3 ISLB/0 CoIS/2 ISLM/0 WebViewType/WK BHT/102 AZPREFIX/az1",
                    "content-type": "application/json",
                    "Accept": "*/*",
                    "Origin": "https://encourage.kuaishou.com",
                    "X-Requested-With": "com.kuaishou.nebula",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Referer": "https://encourage.kuaishou.com/activity/dish?layoutType=4&encourageEventTracking=W3siZW5jb3VyYWdlX3Rhc2tfaWQiOjIwMDA4LCJlbmNvdXJhZ2VfcmVzb3VyY2VfaWQiOiJlYXJuUGFnZV90YXNrTGlzdF8xNyIsImV2ZW50VHJhY2tpbmdMb2dJbmZvIjpbeyJldmVudFRyYWNraW5nVGFza0lkIjoyMDAwOCwicmVzb3VyY2VJZCI6ImVhcm5QYWdlX3Rhc2tMaXN0XzE3IiwiZXh0UGFyYW1zIjp7fX1dfV0",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cookie": token
                }
                resp = requests.get(url, headers=headers)
                resp_json = resp.json()
                if resp_json['result'] == 1:
                    desc = resp_json['data']['popup']['desc']
                    title = resp_json['data']['popup']['title']
                    print(f"{title} {desc}")  
                else:
                    print(resp_json['error_msg'])  
            else:
                print(resp_json['data']['button']['text'])
        else:
            print(resp_json['error_msg'])
    except:
        print(f"获取异常:{traceback.format_exc()}")



def get_qiandao(token):
    print('❤开始执行签到')
    try:
        url = "https://encourage.kuaishou.com/rest/wd/encourage/unionTask/signIn/report?__NS_sig3=2a3a7d4d6842f8f8e6761f757273493c0c023838eaeaf868ce516565636360615e7e&sigCatVer=1"

        # 定义请求头
        headers = {
            "Host": "encourage.kuaishou.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Kwai/13.3.30.9227 ISLP/0 StatusHT/47 KDT/PHONE iosSCH/1 TitleHT/44 NetType/lte ISDM/0 ICFO/0 locale/zh-Hans CT/0 Yoda/3.1.3 ISLB/0 CoIS/2 ISLM/0 WebViewType/WK BHT/102 AZPREFIX/az1",
            "content-type": "application/json",
            "Accept": "*/*",
            "X-Requested-With": "com.kuaishou.nebula",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://encourage.kuaishou.com/kwai/task?layoutType=4&source=pendant&hyId=encourage_earning",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": token
        }

        # 发送 POST 请求
        resp = requests.get(url, headers=headers)
        resp_json = resp.json()
        if resp_json['result'] == 1:
            title = resp_json['data']['reportRewardResult']['awardToast']['title']
            print(f"{title}")
            bsd1 = resp_json['data']['reportRewardResult']['awardToast']['basicSignInAwardResultShow']['bottomText']
            bsd2 = resp_json['data']['reportRewardResult']['awardToast']['basicSignInAwardResultShow']['bottomText']
            print(f"正常：{bsd1}  额外：{bsd2}")
        else:
            print(resp_json['error_msg'])
    except:
        print(f"获取异常:{traceback.format_exc()}")


def main():
    get_qiandao(_cookie)
    get_baoxiang(_cookie)
    #get_fanbu(_cookie)
    get_walk(_cookie)
    get_money(_cookie)

if __name__ == '__main__':
    main()
    send_notification_message(title="快手")

import requests


def postHtmlText(url, data, code='UTF-8'):
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400',
            'Cookie': 'JwOAUserSettingNew='
        }
        r = requests.post(url, data=data, headers=header)
        # print(r.status_code)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print("post获取失败")
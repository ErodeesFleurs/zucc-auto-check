import os
import json
import requests
import datetime


def sign(school_id, password):
    # 获取 JSESSIONID
    school_id = school_id.strip()
    password = password.strip()

    for retryCnt in range(3):
        try:
            url = 'http://ca.zucc.edu.cn/cas/login'
            params = {'service': 'http://yqdj.zucc.edu.cn/feiyan_api/h5/html/daka/daka.html'}
            r = requests.get(url, params, timeout=30)
            cookies = r.cookies.get_dict()
            data = {
                'authType': '0',
                'username': school_id,
                'password': password,
                'lt': '',
                'execution': 'e1s1',
                '_eventId': 'submit',
                'submit': '',
                'randomStr': ''
            }
            url = 'http://ca.zucc.edu.cn/cas/login;jsessionid=' + cookies['JSESSIONID']
            r = requests.post(url, data=data, params=params, cookies=cookies, allow_redirects=False, timeout=30)
            url = r.headers['Location']
            r = requests.get(url, allow_redirects=False, timeout=30)
            cookies = r.cookies.get_dict()
            break
        except Exception as e:
            print(e.__class__.__name__, end='\t')
            if retryCnt < 2:
                print("JSESSIONID 获取失败，正在重试")
            else:
                return "无法获取 JSESSIONID，请检查账号和密码"

    for retryCnt in range(3):
        # 获取问卷
        url = 'http://yqdj.zucc.edu.cn/feiyan_api/examen/examenSchemeController/findExamenSchemeById.do'
        r = requests.post(url, cookies=cookies, data={'esId': 2}, timeout=30)
        questions = json.loads(r.json()['data']['examen']['scheme'])['questions']
        print(questions)
        with open('./data.json', 'w', encoding='utf-8') as file:
            tmp = json.dumps(questions);
            file.write(tmp)

if __name__ == '__main__':
    msg = sign(os.environ["SCHOOL_ID"], os.environ["PASSWORD"])
    print(msg)

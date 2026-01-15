import requests
import random
import http.client
import json
import time
import os
import ssl  # <--- [FIX 1] এইটা নতুন যোগ করেছি
from concurrent.futures import ThreadPoolExecutor

# লাল ওয়ার্নিং বন্ধ করার জন্য
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BOLD = '\033[1m'
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
D = '\033[0m'
C = '\033[96m'

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n            FB File Maker V-2.0\n {D}')

def username_gen(names, start, end):
    usernames = []
    for name in names.split(','):
        for num in range(start, end + 1):
            username = f'{name.strip().lower()}{num} | {name.capitalize()}'
            usernames.append(username)
    return usernames

def checker(uname):
    try:
        headers = {'sec-ch-ua': '\"Chromium\";v=\"139\", \"Not;A=Brand\";v=\"99\"', 'sec-ch-ua-mobile': '?1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36', 'sec-ch-ua-arch': '\"\"', 'Content-Type': 'application/json', 'sec-ch-ua-full-version': '\"139.0.7339.0\"', 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua-platform-version': '\"14.0.0\"', 'Referer': 'https://baji999.net/bd/en/register', 'sec-ch-ua-full-version-list': '\"Chromium\";v=\"139.0.7339.0\", \"Not;A=Brand\";v=\"99.0.0.0\"', 'sec-ch-ua-bitness': '\"\"', 'sec-ch-ua-model': '\"LE2101\"', 'sec-ch-ua-platform': '\"Android\"'}
        
        # <--- [FIX 2] এই লাইনটা যোগ করেছি যাতে SSL চেক না করে
        context = ssl._create_unverified_context()
        
        url = 'https://baji999.net/api/wv/v1/user/registerPreCheck'
        json_data = {'languageTypeId': 1, 'currencyTypeId': 8, 'userId': uname, 'phone': '1347054625', 'friendReferrerCode': '', 'captcha': '', 'callingCode': '880', 'registerTypeId': 0, 'random': str(random.randint(1000, 9999))}
        
        # এখানে context=context বসিয়ে দিয়েছি
        conn = http.client.HTTPSConnection('baji999.net', context=context)
        
        conn.request('POST', '/api/wv/v1/user/registerPreCheck', json.dumps(json_data), headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        if data['status'] == 'F0003':
            return True
        if data['status'] == 'S0001':
            print(f'{R} [RATE LIMIT] PLEASE TURN OFF DATA FOR 10 SEC...!{D}')
            time.sleep(30)
            return False
    except Exception as e:
        # time.sleep(10)
        # print(f'{R} ERROR >> {e}{D}')
        return False
    return False

def check_username(username):
    uname = username.replace(' ', '').split('|')[0]
    if checker(uname):
        print(f'{BOLD}{G} [FB] {uname}{D}')
        with open('.uids.txt', 'a') as file:
            file.write(username + '\n')

def main():
    logo()
    print(f'{BOLD}{Y} ENTER NAMES BY USING COMMA (,) Eg : (Sadek,Tanvir, Sagor) Etc{D}\n')
    names = input(f'{BOLD}{G} ENTER NAMES : {D}')
    print('')
    try:
        start = int(input(f'{BOLD}{Y} START (Eg : 1 ) : '))
        end = int(input(f'{BOLD}{Y} END (Eg : 10000 ) : '))
    except:
        start = 1
        end = 100
        
    print('')
    print(f'{G} [1] LOW SPEED')
    print(f'{Y} [2] MEDIUM SPEED')
    print(f'{R} [3] HIGH SPEED{D}\n')
    print('')
    try:
        speed = int(input(f'{C} CHOOSE : {D}'))
    except:
        speed = 1
        
    if speed == 1:
        spd = 3
    elif speed == 2:
        spd = 6
    elif speed == 3:
        spd = 12
    else:
        spd = 3
    clear_file()
    usernames = username_gen(names, start, end)
    random.shuffle(usernames)
    print('')
    print(f'{BOLD}{G} TOTAL USERNAMES : {len(usernames)} {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')
    with ThreadPoolExecutor(max_workers=spd) as executor:
        executor.map(check_username, usernames)
    print(f'{BOLD}{G} ---------------------------------------{D}')
    total = sum((1 for _ in open('.uids.txt')))
    print(f'\n{BOLD}{G} TOTAL{Y}{total}{G} VALID FB IDS FOUND{D}\n\n')

def clear_file():
    with open('.uids.txt', 'w') as file:
        pass

def switch():
    try:
        # <--- [FIX 3] এখানে verify=False দিয়েছি
        s = requests.get('https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch', verify=False).text
        if 'ON' in s:
            return
        print(f'\n{BOLD}{R} THIS TOOL HAS DISABLED BY ADMIN!{D}')
        exit(0)
    except:
        pass

def setup_username():
    try:
        with open('.name.txt') as f:
            if f.read().strip():
                return
    except FileNotFoundError:
        username = input(f'{Y} ENTER TELEGRAM USERNAME: {D}').strip()
        if not username.startswith('@'):
            username = '@' + username
        with open('.name.txt', 'w') as f:
            f.write(username)

if __name__ == '__main__':
    setup_username()
    switch()
    main()

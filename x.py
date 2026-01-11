
import requests
import random
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor

# ANSI Colors
BOLD, R, G, Y, D, C = '\033[1m', '\033[91m', '\033[92m', '\033[93m', '\033[0m', '\033[96m'

# গ্লোবাল সেশন অবজেক্ট (স্পিড বাড়ানোর জন্য)
session = requests.Session()

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n            FB File Maker V-2.5 (Super Fast)\n {D}')

def username_gen(names, start, end):
    usernames = []
    for name in names.split(','):
        for num in range(start, end + 1):
            usernames.append(f'{name.strip().lower()}{num} | {name.strip().capitalize()}')
    return usernames

def checker(uname):
    """কানেকশন ধরে রেখে দ্রুত চেক করার লজিক"""
    url = 'https://baji999.net/api/wv/v1/user/registerPreCheck'
    
    # cxs.py এর হেডার
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        'Referer': 'https://baji999.net/bd/en/register',
        'Origin': 'https://baji999.net',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # ডিজিটাল ফিঙ্গারপ্রিন্ট
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
        # সেশন ব্যবহার করায় এটি অনেক দ্রুত রেসপন্স করবে
        response = session.post(url, headers=headers, json=payload, timeout=8)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'F0003': 
                return True
            if data.get('status') == 'S0001':
                time.sleep(1) # খুব অল্প বিরতি
        elif response.status_code == 403:
            time.sleep(5)
    except:
        pass
    return False

def check_username(username):
    uname = username.split('|')[0].strip()
    if checker(uname):
        print(f'{BOLD}{G} [VALID FB] {uname}{D}')
        with open('.uids.txt', 'a', encoding='utf-8') as f:
            f.write(username + '\n')

def main():
    logo()
    names = input(f'{BOLD}{Y} ENTER NAMES : {D}')
    start = int(input(f'{BOLD}{Y} START : '))
    end = int(input(f'{BOLD}{Y} END : '))
    
    print(f'\n{R} [!] ৩ নাম্বার অপশনে এখন সর্বোচ্চ স্পিড দেওয়া হয়েছে{D}\n')
    print(f'{G} [1] NORMAL')
    print(f'{Y} [2] MEDIUM')
    print(f'{R} [3] SUPER FAST (Max Threads){D}\n')
    
    speed = int(input(f'{C} CHOOSE : {D}'))
    # স্পিড বাড়াতে থ্রেড সংখ্যা ১৫ থেকে ২০ পর্যন্ত বাড়ানো হয়েছে
    spd = {1: 5, 2: 10, 3: 20}.get(speed, 5)
    
    usernames = username_gen(names, start, end)
    random.shuffle(usernames)
    
    print(f'\n{BOLD}{G} TOTAL USERNAMES : {len(usernames)} | SPEED : {spd}X {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')
    
    # Executor map ব্যবহার করে দ্রুত রিকোয়েস্ট প্রসেসিং
    with ThreadPoolExecutor(max_workers=spd) as executor:
        executor.map(check_username, usernames)
        
    if os.path.exists('.uids.txt'):
        total = sum(1 for _ in open('.uids.txt', 'r'))
        print(f'\n{BOLD}{G} DONE! TOTAL {Y}{total}{G} IDS FOUND.{D}\n')

if __name__ == '__main__':
    main()

import requests
import random
import json
import time
import os
import sys
from concurrent.futures import ThreadPoolExecutor

# ANSI Colors
BOLD, R, G, Y, D, C = '\033[1m', '\033[91m', '\033[92m', '\033[93m', '\033[0m', '\033[96m'

# গ্লোবাল সেশন (স্পিড বাড়ানোর জন্য)
session = requests.Session()

# বিভিন্ন ধরনের ইউজার এজেন্ট (ব্লক এড়াতে)
user_agents = [
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; Redmi Note 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36'
]

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n            FB File Maker V-2.6 (Ultra Fast)\n {D}')

def username_gen(names, start, end):
    usernames = []
    for name in names.split(','):
        for num in range(start, end + 1):
            usernames.append(f'{name.strip().lower()}{num} | {name.strip().capitalize()}')
    return usernames

def checker(uname):
    """রোটেশনাল হেডার এবং ফাস্ট সেশন লজিক"""
    url = 'https://baji999.net/api/wv/v1/user/registerPreCheck'
    
    # প্রতি রিকোয়েস্টে র‍্যান্ডম ইউজার এজেন্ট
    ua = random.choice(user_agents)
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': ua,
        'Referer': 'https://baji999.net/bd/en/register',
        'Origin': 'https://baji999.net',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # ডায়নামিক পে-লোড
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
        # টাইমআউট ৫ সেকেন্ড করা হয়েছে যাতে স্লো না হয়
        response = session.post(url, headers=headers, json=payload, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'F0003': 
                return True
            if data.get('status') == 'S0001':
                # রেট লিমিট আসলে ১ সেকেন্ড অপেক্ষা
                time.sleep(1) 
        elif response.status_code == 403:
            # আইপি ব্লক হলে সামান্য বিরতি
            time.sleep(3)
    except:
        pass
    return False

def check_username(username):
    uname = username.split('|')[0].strip()
    if checker(uname):
        # আউটপুট ফরম্যাট সুন্দর করা হয়েছে
        sys.stdout.write(f'\r{G} [VALID] {uname}                               {D}\n')
        with open('.uids.txt', 'a', encoding='utf-8') as f:
            f.write(username + '\n')

def main():
    logo()
    names = input(f'{BOLD}{Y} ENTER NAMES : {D}')
    start = int(input(f'{BOLD}{Y} START : '))
    end = int(input(f'{BOLD}{Y} END : '))
    
    print(f'\n{G} [1] SAFE SPEED (10 Threads)')
    print(f'{Y} [2] FAST SPEED (20 Threads)')
    print(f'{R} [3] ROCKET SPEED (30 Threads){D}\n')
    
    speed = int(input(f'{C} CHOOSE : {D}'))
    # স্পিড অপশন বাড়িয়ে দেওয়া হয়েছে
    spd = {1: 10, 2: 20, 3: 30}.get(speed, 10)
    
    usernames = username_gen(names, start, end)
    random.shuffle(usernames)
    
    print(f'\n{BOLD}{G} TARGET : {len(usernames)} | THREADS : {spd} {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')
    
    # Executor map দিয়ে দ্রুত প্রসেসিং
    with ThreadPoolExecutor(max_workers=spd) as executor:
        executor.map(check_username, usernames)
        
    if os.path.exists('.uids.txt'):
        total = sum(1 for _ in open('.uids.txt', 'r'))
        print(f'\n{BOLD}{G} ----------------------------------------{D}')
        print(f'{BOLD}{G} DONE! TOTAL VALID IDS: {Y}{total}{D}\n')

if __name__ == '__main__':
    main()


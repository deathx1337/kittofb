import requests
import random
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor
import urllib3

# সব ধরণের SSL ওয়ার্নিং বন্ধ করার জন্য
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BOLD = '\033[1m'
R = '\033[91m' # Red
G = '\033[92m' # Green
Y = '\033[93m' # Yellow
D = '\033[0m'  # Default
C = '\033[96m' # Cyan

def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{BOLD}{C}\n       _____ __      ___                \n      / __(_) /__   / _ \\__ ____ _  ___ \n     / _// / / -_) / // / // /  \' \\/ _ \\\n    /_/ /_/_/\\__/ /____/\\_,_/_/_/_/ .__/\n                                 /_/    \n\n            FB File Maker V-2.0 (Requests Version)\n {D}')

def username_gen(names, start, end):
    usernames = []
    for name in names.split(','):
        for num in range(start, end + 1):
            username = f'{name.strip().lower()}{num} | {name.capitalize()}'
            usernames.append(username)
    return usernames

def checker(uname):
    try:
        url = 'https://baji999.net/api/wv/v1/user/registerPreCheck'
        
        # হেডার কিছুটা আপডেট করা হয়েছে যাতে রিয়েল ব্রাউজার মনে হয়
        headers = {
            'Host': 'baji999.net',
            'sec-ch-ua': '"Not A(Brand";v="99", "Android WebView";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://baji999.net/bd/en/register',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-platform': '"Android"',
            'Origin': 'https://baji999.net'
        }
        
        json_data = {
            'languageTypeId': 1,
            'currencyTypeId': 8,
            'userId': uname,
            'phone': '1347054625',
            'friendReferrerCode': '',
            'captcha': '',
            'callingCode': '880',
            'registerTypeId': 0,
            'random': str(random.randint(1000, 9999))
        }

        # requests লাইব্রেরি ব্যবহার করা হচ্ছে (SSL Verify False)
        response = requests.post(url, json=json_data, headers=headers, verify=False, timeout=10)
        
        # রেসপন্স চেক করা
        if response.status_code == 200:
            data = response.json()
            
            # F0003 মানে ইউজার নেম অলরেডি আছে (Success)
            if 'F0003' in str(data): 
                return True
                
            # রেট লিমিট বা আইপি ব্লক
            elif 'S0001' in str(data):
                print(f'{R} [RATE LIMIT] Sleeping for 5s...{D}')
                time.sleep(5)
                return False
            
            # অন্য কোনো রেসপন্স আসলে দেখার জন্য (Debugging)
            # else:
            #     print(f'{R} UNKNOWN RESPONSE: {data}{D}') 
                
        return False

    except requests.exceptions.ConnectionError:
        # নেটওয়ার্ক এরর
        time.sleep(2)
        return False
    except Exception as e:
        # অন্যান্য এরর
        # print(f'{R} Error: {e}{D}')
        return False

def check_username(username):
    # নাম আলাদা করা হচ্ছে
    uname = username.split('|')[0].strip()
    
    if checker(uname):
        print(f'{BOLD}{G} [LIVE] {uname}{D}')
        with open('.uids.txt', 'a') as file:
            file.write(username + '\n')
    else:
        # চেক করার সময় দেখার জন্য (অপশনাল)
        print(f'{R} [BAD]  {uname}{D}', end='\r')

def main():
    logo()
    print(f'{BOLD}{Y} ENTER NAMES BY USING COMMA (,) Eg : (Sadek,Tanvir, Sagor) Etc{D}\n')
    names = input(f'{BOLD}{G} ENTER NAMES : {D}')
    print('')
    try:
        start = int(input(f'{BOLD}{Y} START (Eg : 1 ) : '))
        end = int(input(f'{BOLD}{Y} END (Eg : 10000 ) : '))
    except ValueError:
        print("Invalid Input")
        return

    print('')
    print(f'{G} [1] LOW SPEED')
    print(f'{Y} [2] MEDIUM SPEED')
    print(f'{R} [3] HIGH SPEED{D}\n')
    
    try:
        speed = int(input(f'{C} CHOOSE : {D}'))
    except:
        speed = 1
        
    if speed == 1: spd = 5
    elif speed == 2: spd = 10
    elif speed == 3: spd = 20
    else: spd = 5
    
    clear_file()
    usernames = username_gen(names, start, end)
    random.shuffle(usernames)
    
    print('')
    print(f'{BOLD}{G} TOTAL USERNAMES : {len(usernames)} {D}')
    print(f'{BOLD}{G} ----------------------------------------{D}')
    
    with ThreadPoolExecutor(max_workers=spd) as executor:
        executor.map(check_username, usernames)
        
    print(f'{BOLD}{G} ---------------------------------------{D}')
    try:
        total = sum((1 for _ in open('.uids.txt')))
        print(f'\n{BOLD}{G} TOTAL{Y} {total} {G}VALID FB IDS FOUND{D}\n\n')
    except:
        print("No ids found")

def clear_file():
    with open('.uids.txt', 'w') as file:
        pass

def switch():
    try:
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

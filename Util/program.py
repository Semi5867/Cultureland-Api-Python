import os, string, random, time, clipboard, platform, requests
from datetime import timedelta, datetime

def pick(_LENGTH):
    string_pool = string.ascii_letters + string.digits
    result = "" 
    for i in range(_LENGTH) :
        result += random.choice(string_pool)
    return result

def is_expired(time):
    ServerTime = datetime.now()
    ExpireTime = datetime.strptime(time, '%Y-%m-%d %H:%M')
    if ((ExpireTime - ServerTime).total_seconds() > 0):
        return False
    else:
        return True

def get_expiretime(time):
    ServerTime = datetime.now()
    ExpireTime = datetime.strptime(time, '%Y-%m-%d %H:%M')
    if ((ExpireTime - ServerTime).total_seconds() > 0):
        how_long = (ExpireTime - ServerTime)
        days = how_long.days
        hours = how_long.seconds // 3600
        minutes = how_long.seconds // 60 - hours * 60
        return str(round(days)) + "일 " + str(round(hours)) + "시간 " + str(round(minutes)) + "분" 
    else:
        return False

def make_expiretime(days):
    ServerTime = datetime.now()
    ExpireTime = ServerTime + timedelta(days=days)
    ExpireTime_STR = ExpireTime.strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR

def add_time(now_days, add_days):
    ExpireTime = datetime.strptime(now_days, '%Y-%m-%d %H:%M')
    ExpireTime_STR = (ExpireTime + timedelta(days=add_days)).strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR

def clear():
    try:
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
    except:
        pass

def print_banner():
    print()
    print()
    print('''  /$$$$$$                          /$$        /$$$$$$            /$$
 /$$__  $$                        |__/       /$$__  $$          |__/
| $$  \__/  /$$$$$$  /$$$$$$/$$$$  /$$      | $$  \ $$  /$$$$$$  /$$
|  $$$$$$  /$$__  $$| $$_  $$_  $$| $$      | $$$$$$$$ /$$__  $$| $$
 \____  $$| $$$$$$$$| $$ \ $$ \ $$| $$      | $$__  $$| $$  \ $$| $$
 /$$  \ $$| $$_____/| $$ | $$ | $$| $$      | $$  | $$| $$  | $$| $$
|  $$$$$$/|  $$$$$$$| $$ | $$ | $$| $$      | $$  | $$| $$$$$$$/| $$
 \______/  \_______/|__/ |__/ |__/|__/      |__/  |__/| $$____/ |__/
                                                      | $$          
                                                      | $$          
                                                      |__/         ''')
    print()
    print()
    return

def main():
    clear()
    print_banner()
    print("[1] Generate Api Key")
    print("[2] Delete Api Key")
    print("[3] Lookup Api Key")
    print("[4] White IP")
    print("[5] Unwhite IP")
    try:
        choice = int(input("[~] Your Choice : "))
    except:
        print("[-] 정수로만 입력해주세요.")
        time.sleep(1)
        main()
    clear()
    if choice == 1:
        try:
            length = int(input('[~] Api Key Length : '))
            amount = int(input('[~] Api Key Amount : '))
            pw = input("[~] Password To Access The Api : ")
        except:
            print("[-] 정수로만 입력해주세요.")
            time.sleep(1)
            main()
        clear()
        res = requests.post("도메인/admin/api", json={'edit_type': 'generate', 'length': length, 'amount': amount, 'pw': pw})
        if res.json()['result'] == True:
            keys = "\n".join(res.json()['keys'])
            clipboard.copy(keys)
            print("[+] Succeeded To Copy The Api Keys To Your Clipboard")
            for key in res.json()['keys']:
                print(f"{key}")
            input("[~] Press Any Key To Return To Main")
            main()
        else:
            print("[-] Failed To Copy The Api Keys To Your Clipboard")
            print(f"[-] Reason : {res.json()['reason']}")
            input("[~] Press Any Key To Return To Main")
            main()
    elif choice == 2:
        try:
            key = input('[~] Api Key To Delete : ')
            pw = input("[~] Password To Access The Api : ")
        except:
            print("[-] 정수로만 입력해주세요.")
            time.sleep(1)
            main()
        clear()
        res = requests.post("도메인/admin/api", json={'edit_type': 'delete', 'key': key, 'pw': pw})
        if res.json()['result'] == True:
            print("[+] Succeeded To Delete The Api Key In Database")
            input("[~] Press Any Key To Return To Main")
            main()
        else:
            print("[-] Failed To Delete The Api Key In Database")
            print(f"[-] Reason : {res.json()['reason']}")
            input("[~] Press Any Key To Return To Main")
            main()
    elif choice == 3:
        try:
            key = input('[~] Api Key To Lookup : ')
            pw = input("[~] Password To Access The Api : ")
        except:
            print("[-] 정수로만 입력해주세요.")
            time.sleep(1)
            main()
        clear()
        res = requests.post("도메인/admin/api", json={'edit_type': 'lookup', 'key': key, 'pw': pw})
        if res.json()['result'] == True:
            print("[+] Succeeded To Lookup The Api Key")
            for user in res.json()['users']:
                print(f"{user[0]}    {user[1]}    {user[2]}    {user[3]}")
            input("[~] Press Any Key To Return To Main")
            main()
        else:
            print("[-] Failed To Lookup The Api Key")
            print(f"[-] Reason : {res.json()['reason']}")
            input("[~] Press Any Key To Return To Main")
            main()
    elif choice == 4:
        ip = input('[~] IP To White : ')
        pw = input("[~] Password To Access The Api : ")
        res = requests.post("도메인/admin/api", json={'edit_type': 'white', 'ip': ip, 'pw': pw})
        if res.json()['result'] == True:
            print("[+] Succeeded To White The IP")
            print(ip)
            input("[~] Press Any Key To Return To Main")
            main()
        else:
            print("[-] Failed To White The IP")
            print(f"[-] Reason : {res.json()['reason']}")
            input("[~] Press Any Key To Return To Main")
            main()
    elif choice == 5:
        ip = input('[~] IP To Unwhite : ')
        pw = input("[~] Password To Access The Api : ")
        res = requests.post("도메인/admin/api", json={'edit_type': 'unwhite', 'ip': ip, 'pw': pw})
        if res.json()['result'] == True:
            print("[+] Succeeded To Unwhite The IP")
            print(ip)
            input("[~] Press Any Key To Return To Main")
            main()
        else:
            print("[-] Failed To Unwhite The IP")
            print(f"[-] Reason : {res.json()['reason']}")
            input("[~] Press Any Key To Return To Main")
            main()
    else:
        print("[-] Please Choose In 1 to 5")
        time.sleep(1)
        main()

if __name__ == "__main__":
    main()
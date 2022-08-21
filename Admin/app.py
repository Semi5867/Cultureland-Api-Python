import sqlite3, logging, random, string, requests
from flask import Flask, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta, datetime
from cultureland import *

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
log.disabled = True

class cprint:
    def __init__(self, text):
        self.text = text

    def black(self):
        print(f"\033[30m{self.text}\033[0m")

    def red(self):
        print(f"\033[31m{self.text}\033[0m")

    def green(self):
        print(f"\033[32m{self.text}\033[0m")

    def yellow(self):
        print(f"\033[33m{self.text}\033[0m")

    def blue(self):
        print(f"\033[34m{self.text}\033[0m")

    def magenta(self):
        print(f"\033[35m{self.text}\033[0m")

    def cyan(self):
        print(f"\033[36m{self.text}\033[0m")

    def white(self):
        print(f"\033[37m{self.text}\033[0m")

    def bright_black(self):
        print(f"\033[90m{self.text}\033[0m")

    def bright_red(self):
        print(f"\033[91m{self.text}\033[0m")

    def bright_green(self):
        print(f"\033[92m{self.text}\033[0m")
        
    def bright_yellow(self):
        print(f"\033[93m{self.text}\033[0m")

    def bright_blue(self):
        print(f"\033[94m{self.text}\033[0m")

    def bright_magenta(self):
        print(f"\033[95m{self.text}\033[0m")

    def bright_cyan(self):
        print(f"\033[96m{self.text}\033[0m")

    def bright_white(self):
        print(f"\033[97m{self.text}\033[0m")

def get_ip():
    return request.environ.get("HTTP_X_REAL_IP", request.remote_addr)

def get_time():
    return str(datetime.now())[:-7]

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

def get_user_info(cid):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE cid = ?;", (cid,))
    result = cur.fetchone()
    con.close()
    return result

def get_white_list():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM whites;")
    result = []
    for i in cur.fetchall():
        result.append(i[0])
    con.close()
    return result

def pick(_LENGTH):
    string_pool = string.ascii_letters + string.digits
    result = "" 
    for i in range(_LENGTH) :
        result += random.choice(string_pool)
    return result

@app.route("/admin/api", methods=["POST"])
def edit_api():
    obj = request.get_json()
    edit_type = obj.get('edit_type')
    if edit_type == "generate":
        length = obj.get('length')
        amount = obj.get('amount')
        pw = obj.get('pw')
        if pw == None or length == None or amount == None:
            result = {'result': False, 'reason': '값이 틀립니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_red()
            return result
        elif pw != "semiisadmin":
            result = {'result': False, 'reason': '비밀번호가 틀립니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_red()
            return result
        keys = []
        for i in range(amount):
            api_key = pick(15)
            con = sqlite3.connect("./database.db")
            cur = con.cursor()
            cur.execute("INSERT INTO apis VALUES(?, ?);", (api_key, make_expiretime(length)))
            con.commit()
            con.close()
            keys.append(api_key)
        result = {'result': True, 'keys': keys}
        cprint(f"[SUCCEEDED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_green()
        return result
    elif edit_type == "delete":
        key = obj.get('key')
        pw = obj.get('pw')
        if pw == None or key == None:
            result = {'result': False, 'reason': '값이 틀립니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_red()
            return result
        elif pw != "semiisadmin":
            result = {'result': False, 'reason': '비밀번호가 틀립니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_red()
            return result
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM apis WHERE token = ?;", (key,))
        token_info = cur.fetchone()
        con.close()
        if token_info == None:
            result = {'result': False, 'reason': 'API KEY가 존재하지 않습니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_red()
            return result
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("DELETE FROM apis WHERE token = ?;", (key,))
        con.commit()
        cur.execute("DELETE FROM users WHERE token = ?;", (key,))
        con.commit()
        con.close()
        result = {'result': True}
        cprint(f"[SUCCEEDED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_green()
        return result
    elif edit_type == "lookup":
        key = obj.get('key')
        pw = obj.get('pw')
        if pw == None or key == None:
            result = {'result': False, 'reason': '값이 틀립니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_red()
            return result
        elif pw != "semiisadmin":
            result = {'result': False, 'reason': '비밀번호가 틀립니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_red()
            return result
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM apis WHERE token = ?;", (key,))
        token_info = cur.fetchone()
        con.close()
        if token_info == None:
            result = {'result': False, 'reason': 'API KEY가 존재하지 않습니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_red()
            return result
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE token = ?;", (key,))
        users = cur.fetchall()
        con.close()
        result = {'result': True, 'users': users}
        cprint(f"[SUCCEEDED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_green()
        return result
    elif edit_type == "white":
        ip = obj.get('ip')
        pw = obj.get('pw')
        if pw == None or ip == None:
            result = {'result': False, 'reason': '값이 틀립니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_red()
            return result
        elif pw != "semiisadmin":
            result = {'result': False, 'reason': '비밀번호가 틀립니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_red()
            return result
        headers = {
            'authority': 'ipinfo.io',
            'accept': '*/*',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'referer': 'https://ipinfo.io/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }
        ip_info = requests.get(f"https://ipinfo.io/widget/demo/{ip}", headers=headers)
        if ip_info.status_code != 200:
            result = {'result': False, 'reason': 'IP가 잘못되었습니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_red()
            return result
        white_list = get_white_list()
        if ip in white_list:
            result = {'result': False, 'reason': '해당 IP는 이미 등록되어있습니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_red()
            return result
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("INSERT INTO whites VALUES(?);", (ip,))
        con.commit()
        con.close()
        result = {'result': True, 'reason': '해당 IP가 등록되었습니다.'}
        cprint(f"[SUCCEEDED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_green()
        return result
    elif edit_type == "unwhite":
        ip = obj.get('ip')
        pw = obj.get('pw')
        if pw == None or ip == None:
            result = {'result': False, 'reason': '값이 틀립니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_red()
            return result
        elif pw != "semiisadmin":
            result = {'result': False, 'reason': '비밀번호가 틀립니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_red()
            return result
        white_list = get_white_list()
        if not ip in white_list:
            result = {'result': False, 'reason': '해당 IP는 이미 제거되었거나 등록되어있지 않습니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_red()
            return result
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("DELETE FROM whites WHERE ip = ?;", (ip,))
        con.commit()
        con.close()
        result = {'result': True, 'reason': '해당 IP가 제거되었습니다.'}
        cprint(f"[SUCCEEDED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_green()
        return result
    else:
        result = {'result': False, 'reason': 'EDIT_TYPE이 올바르지 않습니다.'}
        cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - ADMIN_Semi").bright_red()
        return result


@app.route("/balance", methods=["POST"])
@limiter.limit("3/minute")
def balance():
    obj = request.get_json()
    cid = obj.get("id")
    cpw = obj.get("pw")
    token = obj.get("token")
    if cid == None or cpw == None or token == None:
        result = {'result': False, 'reason': '값이 틀립니다.'}
        cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - {token}").bright_red()
        return result
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM apis WHERE token = ?;", (token,))
    token_info = cur.fetchone()
    con.close()
    if token_info != None:
        if is_expired(token_info[1]) == False:
            re = cultureland(cid, cpw)
            a = re.login()
            if a['result'] == False:
                cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {a} - {token}").bright_red()
                return a
            getbalance = re.getbalance()
            if getbalance['result'] == True:
                userinfo = get_user_info(cid)
                if userinfo == None:
                    con = sqlite3.connect("database.db")
                    cur = con.cursor()
                    cur.execute("INSERT INTO users VALUES(?, ?, ?);", (token, cid, cpw))
                    con.commit()
                    con.close()
                else:
                    if userinfo[2] != cpw:
                        con = sqlite3.connect("database.db")
                        cur = con.cursor()
                        cur.execute("UPDATE users SET cpw = ? WHERE cid = ?;", (cpw, cid))
                        con.commit()
                        con.close()
                cprint(f"[SUCCEEDED] {get_ip()} - [{get_time()}] - {getbalance} - {token}").bright_green()
                return getbalance
            else:
                cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {getbalance} - {token}").bright_red()
                return getbalance
        else:
            result = {'result': False, 'reason': '만료된 API키입니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - {token}").bright_red()
            return result
    else:
        result = {'result': False, 'reason': 'API키가 틀립니다.'}
        cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - {token}").bright_red()
        return result

@app.route("/charge", methods=["POST"])
@limiter.limit("3/minute")
def charge():
    obj = request.get_json()
    cid = obj.get("id")
    cpw = obj.get("pw")
    token = obj.get("token")
    pin = obj.get('pin')
    if cid == None or cpw == None or token == None or pin == None:
        result = {'result': False, 'fake': False, 'reason': '값이 틀립니다.'}
        cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - {token}").bright_red()
        return result
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM apis WHERE token = ?;", (token,))
    token_info = cur.fetchone()
    con.close()
    if token_info != None:
        if is_expired(token_info[1]) == False:
            re = cultureland(cid, cpw)
            a = re.login()
            if a['result'] == False:
                cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {a} - {token}").bright_red()
                return a
            charge = re.charge(pin)
            if charge['result'] == True:
                userinfo = get_user_info(cid)
                if userinfo == None:
                    con = sqlite3.connect("database.db")
                    cur = con.cursor()
                    cur.execute("INSERT INTO users VALUES(?, ?, ?);", (token, cid, cpw))
                    con.commit()
                    con.close()
                else:
                    if userinfo[2] != cpw:
                        con = sqlite3.connect("database.db")
                        cur = con.cursor()
                        cur.execute("UPDATE users SET cpw = ? WHERE cid = ?;", (cpw, cid))
                        con.commit()
                        con.close()
                cprint(f"[SUCCEEDED] {get_ip()} - [{get_time()}] - {charge} - {token}").bright_green()
                return charge
            else:
                cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {charge} - {token}").bright_red()
                return charge
        else:
            result = {'result': False, 'fake': False, 'reason': '만료된 API키입니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - {token}").bright_red()
            return result
    else:
        result = {'result': False, 'fake': False, 'reason': 'API키가 틀립니다.'}
        cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - {token}").bright_red()
        return result

@app.route("/gift", methods=["POST"])
@limiter.limit("3/minute")
def gift():
    obj = request.get_json()
    cid = obj.get("id")
    cpw = obj.get("pw")
    token = obj.get("token")
    amount = obj.get('amount')
    if cid == None or cpw == None or token == None or amount == None:
        result = {'result': False, 'reason': '값이 틀립니다.'}
        cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - {token}").bright_red()
        return result
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM apis WHERE token = ?;", (token,))
    token_info = cur.fetchone()
    con.close()
    if token_info != None:
        if is_expired(token_info[1]) == False:
            re = cultureland(cid, cpw)
            a = re.login()
            if a['result'] == False:
                cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {a} - {token}").bright_red()
                return a
            gift = re.gift(amount)
            if gift['result'] == True:
                userinfo = get_user_info(cid)
                if userinfo == None:
                    con = sqlite3.connect("database.db")
                    cur = con.cursor()
                    cur.execute("INSERT INTO users VALUES(?, ?, ?);", (token, cid, cpw))
                    con.commit()
                    con.close()
                else:
                    if userinfo[2] != cpw:
                        con = sqlite3.connect("database.db")
                        cur = con.cursor()
                        cur.execute("UPDATE users SET cpw = ? WHERE cid = ?;", (cpw, cid))
                        con.commit()
                        con.close()
                cprint(f"[SUCCEEDED] {get_ip()} - [{get_time()}] - {gift} - {token}").bright_green()
                return gift
            else:
                cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {gift} - {token}").bright_red()
                return gift
        else:
            result = {'result': False, 'reason': '만료된 API키입니다.'}
            cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - {token}").bright_red()
            return result
    else:
        result = {'result': False, 'reason': 'API키가 틀립니다.'}
        cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result} - {token}").bright_red()
        return result

@app.errorhandler(404)
def ratelimit_handler(e):
    result = {'result': False, 'fake': False, 'reason': '주소가 잘못되었습니다.'}
    cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result}").bright_red()
    return result

@app.errorhandler(405)
def ratelimit_handler(e):
    result = {'result': False, 'fake': False, 'reason': '요청 종류가 잘못되었습니다.'}
    cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result}").bright_red()
    return result

@app.errorhandler(429)
def ratelimit_handler(e):
    result = {'result': False, 'fake': False, 'reason': '요청이 너무 많습니다, 나중에 다시 시도해주세요.'}
    cprint(f"[FAILED] {get_ip()} - [{get_time()}] - {result}").bright_red()
    return result

@app.before_request
def limit_remote_addr():
    white_list = get_white_list()
    ip = get_ip()
    if not ip in white_list:
        abort(403)

if __name__ == "__main__":
    app.run("0.0.0.0", port=80)

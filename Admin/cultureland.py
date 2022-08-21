from datetime import datetime
from selectolax.lexbor import LexborHTMLParser
from requests import session, Response
from mTransKey.transkey import mTransKey

class cultureland:
    def __init__(self, username, password):
        self.sess = session()
        self.username = username
        self.password = password

    def login(self):
        username = self.username
        password = self.password
        if len(username) > 12 or len(username) < 6 or username is None or username == "" or len(password) > 12 or len(password) < 6 or password is None or password == "":
            return {'result': False, 'reason': '아이디 또는 비밀번호의 형식이 틀립니다.'}
        self.mtk = mTransKey(self.sess)
        pw_pad = self.mtk.new_keypad("qwerty", "passwd", "passwd", "password")
        encrypted = pw_pad.encrypt_password(password)
        hm = self.mtk.hmac_digest(encrypted.encode())
        data = {"agentUrl": "", "returnUrl": "", "keepLoginInfo": "", "phoneForiOS": "", "hidWebType": "other", "userId": username, "passwd": "*"*len(password), "transkeyUuid":  self.mtk.get_uuid(), "transkey_passwd": encrypted, "transkey_HM_passwd": hm}
        res: Response = self.sess.post("https://m.cultureland.co.kr/mmb/loginProcess.do", data=data, cookies={'KeepLoginConfig': 'lkjasf'})
        if not res.status_code == 200:
            return {'result': False, 'reason': '상태 코드가 틀립니다.'}
        if '입력하신 아이디 또는 비밀번호가 틀립니다' in res.text:
            return {'result': False, 'reason': '입력하신 아이디 또는 비밀번호가 틀립니다.'}
        res: Response = self.sess.post("https://m.cultureland.co.kr/mmb/isLogin.json")
        if res.text == 'false':
            return {'result': False, 'reason': '로그인에 실패하였습니다.'}
        elif res.text == 'true':
            return {'result': True}
        return {'result': False, 'reason': '알 수 없는 오류 1.'}

    def getbalance(self):
        res: Response = self.sess.post("https://m.cultureland.co.kr/gft/chkGiftLimitAmt.json")
        if not res.status_code == 200:
            return {'result': False, 'reason': '상태 코드가 틀립니다.'}
        chkGiftLimitAmt = res.json()
        try:
            if chkGiftLimitAmt['errMsg'] == '정상':
                giftVO = chkGiftLimitAmt['giftVO']
                return {'result': True, 'balanceAmt': int(giftVO['balanceAmt']), 'safeAmt': int(giftVO['safeAmt']), 'ccashRemainAmt': int(giftVO['ccashRemainAmt'])}
        except:
            if chkGiftLimitAmt['resultMessage'] == "로그인이 필요한 서비스 입니다.":
                return {'result': False, 'reason': '로그인이 필요한 서비스 입니다.'}
        return {'result': False, 'reason': '알 수 없는 오류 2.'}

    def charge(self, code: str=None):
        if code is None:
            return {'result': False, 'fake': False, 'reason': '문화상품권 핀번호를 입력해주세요.'}
        res: Response = self.sess.get("https://m.cultureland.co.kr/csh/cshGiftCard.do")
        if not res.status_code == 200:
            return {'result': False, 'fake': False, 'reason': '상태 코드가 틀립니다.'}
        codes = code.split("-")
        if len(codes) != 4:
            codes = code.split(" ")
        if len(codes) != 4:
            return {'result': False, 'fake': True, 'reason': '상품권 번호 형식이 틀립니다. 1'}
        elif code.startswith("1") or code.startswith("6") or code.startswith("7") or code.startswith("0"):
            return {'result': False, 'fake': True, 'reason': '상품권 번호 형식이 틀립니다. 2'}
        elif code.startswith("41") and len(codes[3]) != 4:
            return {'result': False, 'fake': True, 'reason': '상품권 번호 형식이 틀립니다. 3'}
        elif code.startswith("20") and len(codes[3]) != 6:
            return {'result': False, 'fake': True, 'reason': '상품권 번호 형식이 틀립니다. 4'}
        elif code.startswith("21") and len(codes[3]) != 6:
            return {'result': False, 'fake': True, 'reason': '상품권 번호 형식이 틀립니다. 5'}
        elif code.startswith("22") and len(codes[3]) != 6:
            return {'result': False, 'fake': True, 'reason': '상품권 번호 형식이 틀립니다. 6'}
        elif code.startswith("30") and len(codes[3]) != 6:
            return {'result': False, 'fake': True, 'reason': '상품권 번호 형식이 틀립니다. 7'}
        elif code.startswith("31") and len(codes[3]) != 6:
            return {'result': False, 'fake': True, 'reason': '상품권 번호 형식이 틀립니다. 8'}
        elif code.startswith("32") and len(codes[3]) != 6:
            return {'result': False, 'fake': True, 'reason': '상품권 번호 형식이 틀립니다. 9'}
        elif code.startswith("40") and len(codes[3]) != 6:
            return {'result': False, 'fake': True, 'reason': '상품권 번호 형식이 틀립니다. 10'}
        elif code.startswith("42") and len(codes[3]) != 6:
            return {'result': False, 'fake': True, 'reason': '상품권 번호 형식이 틀립니다. 11'}
        elif code.startswith("51") and len(codes[3]) != 6:
            return {'result': False, 'fake': True, 'reason': '상품권 번호 형식이 틀립니다. 12'}
        elif code.startswith("52") and len(codes[3]) != 6:
            return {'result': False, 'fake': True, 'reason': '상품권 번호 형식이 틀립니다. 13'}
        txt1_pad = self.mtk.new_keypad("number", "txtScr14", "scr14", "password")
        txt1_encrypted = txt1_pad.encrypt_password(codes[3])
        txt1_hm = self.mtk.hmac_digest(txt1_encrypted.encode())
        data = { "scr11": codes[0], "scr12": codes[1], "scr13": codes[2], "scr14": "*" * len(codes[3]), "transkeyUuid": self.mtk.get_uuid(), "transkey_txtScr14": txt1_encrypted, "transkey_HM_txtScr14": txt1_hm }
        res: Response = self.sess.post("https://m.cultureland.co.kr/csh/cshGiftCardProcess.do", data=data)
        parser = LexborHTMLParser(res.text)
        result = parser.root.css_first("b").text()
        if result == '충전 완료':
            amount = int(parser.root.css_first("dd").text().replace("원", "").replace(",", ""))
            return {'result': True, 'fake': False, 'amount': amount}
        else:
            return {'result': False, 'fake': False, 'reason': result}
        return {'result': False, 'fake': False, 'reason': '알 수 없는 오류 3.'}

    def gift(self, amount: str=None):
        if amount is None:
            return {'result': False, 'reason': '금액을 입력해주세요.'}
        if not amount.isdigit() or int(amount) < 1:
            return {'result': False, 'reason': '금액은 양수, 정수여야 합니다.'}
        if int(amount) < 1000:
            return {'result': False, 'reason': '최소 금액은 1000원 입니다.'}
        res: Response = self.sess.get("https://m.cultureland.co.kr/gft/gftPhoneApp.do")
        if not res.status_code == 200:
            return {'result': False, 'reason': '상태 코드가 틀립니다.'}
        if '월 1회 휴대폰 본인인증이 필요' in res.text:
            return {'result': False, 'reason': '월 1회 휴대폰 본인인증이 필요합니다.'}
        elif '가입 유형' in res.text and '이메일인증회원' in res.text:
            return {'result': False, 'reason': '이메일 인증회원은 환전이 불가능합니다.'}
        elif not '선물(구매) 금액 직접 입력(원)' in res.text:
            return {'result': False, 'reason': '알 수 없는 오류 4.'}
        getbalance = self.getbalance()
        if getbalance['result'] == False:
            return getbalance
        if getbalance['balanceAmt'] == 0 and not getbalance['safeAmt'] == 0:
            return {'result': False, 'reason': '보관중인 금액을 찾아주세요.'}
        if getbalance['balanceAmt'] < int(amount) or getbalance['balanceAmt'] == 0:
            return {'result': False, 'reason': '잔액이 부족합니다.'}
        if getbalance['ccashRemainAmt'] == 0:
            return {'result': False, 'reason': '컬쳐캐쉬 한도 초과입니다.'}
        if getbalance['ccashRemainAmt'] < int(amount):
            return {'result': False, 'reason': '컬쳐캐쉬 한도보다 금액이 큽니다.'}
        flagSecCash_res: Response = self.sess.post("https://m.cultureland.co.kr/tgl/flagSecCash.json")
        flagSecCash = flagSecCash_res.json()
        if flagSecCash['resultMessage'] == '로그인이 필요한 서비스 입니다.':
            return {'result': False, 'reason': '로그인에 실패하였습니다.'}
        elif not flagSecCash['resultMessage'] == "성공":
            return {'result': False, 'reason': '알 수 없는 오류 5.'}
        self.sess.get("https://m.cultureland.co.kr/gft/gftPhoneApp.do")
        res: Response = self.sess.post("https://m.cultureland.co.kr/gft/gftPhoneCashProc.do", data={ "revEmail": "", "sendType": "S", "userKey": flagSecCash["userKey"], "limitGiftBank": "N", "giftCategory": "M", "amount": amount, "quantity": "1", "revPhone": flagSecCash['Phone'], "sendTitl": "gea",  "paymentType": "cash" })
        text = res.text
        if '잔액이 부족합니다.' in text:
            return {'result': False, 'reason': '잔액이 부족합니다.'}
        elif '(주)한국문화진흥의 신용으로 발행한 상품권입니다.' in text:
            parser = LexborHTMLParser(text)
            input = parser.root.css_first("#mmsSb")
            value: str = input.attrs['value'].replace('- ', '')
            data = value.split('<br>')
            link = data[0].replace('상품권 바로 충전 : ', '')
            amount = data[7].replace('금액 : ', '').replace(',', '').replace('원', '')
            giftpin = data[8].replace('바코드번호 : ', '')
            expiredate = data[9].replace('유효기간 : ', '')
            return {'result': True, 'link': link, 'amount': amount, 'giftpin': giftpin, 'expiredate': expiredate}
        elif '23시 50분부터 0시 10분까지는 시스템 점검 시간이므로 잠시후에 이용하시기 바랍니다.' in text:
            return {'result': False, 'reason': '현재 시스템 점검으로 인해 사용이 불가하므로 잠시후에 이용하시기 바랍니다.'}
        return {'result': False, 'reason': '알 수 없는 오류 6.'}

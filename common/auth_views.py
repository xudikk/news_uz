import random
import uuid

import requests
from django.conf import settings
from django.contrib.auth import login, authenticate, logout as lout
from django.shortcuts import render, redirect

from common.models import User, Otp
import requests
from methodism.helper import code_decoder, generate_key


def send_sms(code):
    url = "https://notify.eskiz.uz/api/message/sms/send"
    payload = {
        'mobile_phone': '998935278284',
        'message': f'Bu Eskiz dan test',
        'from': '4546',
        'callback_url': 'http://0000.uz/test.php'
    }
    files = [
    ]
    headers = {
        "Authorization": f"Bearer {settings.ESKIZ_TOKEN}"
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response)
    print(response.text)


def auth(request):
    if not request.user.is_anonymous:
        return redirect("home")

    if request.POST:
        key = request.POST.get("login", None)
        data = request.POST
        extra = {}
        if key:
            phone = data.get("login_phone", None)
            pas = data.get("login_pass", None)

            user = User.objects.filter(phone=phone).first()
            if not user:
                return render(request, "auth/login.html", {"error": "Phone Yoki Parol Xato"})
            if not user.is_active:
                return render(request, "auth/login.html", {"error": "Ushbu User Blocklangan"})

            if not user.check_password(str(pas)):
                return render(request, "auth/login.html", {"error": "Phone Yoki Parol Xato"})
            # OTP yaratishimiz kerak



        else:
            # regis qilishim kerak
            phone = data.get('regis_phone', None)
            full_name = data.get("regis_fullname", None)
            regis_pass = data.get("regis_pass", None)
            regis_pass_conf = data.get("regis_pass_conf", None)

            if None in [phone, full_name, regis_pass, regis_pass_conf]:
                return render(request, "auth/login.html", {"error": "Hammasini to'ldiring"})

            if regis_pass != regis_pass_conf:
                return render(request, "auth/login.html", {"error": "Parollar Har xil"})

            user = User.objects.filter(phone=phone).first()
            if user:
                return render(request, "auth/login.html", {"error": "User Allaqachon bor"})

            extra = {
                "fullname": full_name,
                "password": regis_pass
            }



        # OTP shu yerda yaratamiz -> phone
        code = random.randint(100_000, 999_999)  # 125854
        # send_sms(code)
        # srazi sms bo'p chiqib ketadi
        # message = f"Sizning OTP kodingiz: {code}"
        # url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={727652365}&text={message}"
        # requests.get(url)

        # heshlash -> shifrlash (static, dinamik)
        unical = uuid.uuid4()  # uzun token hosil qiladi
        gen_code = generate_key(15)
        natija = f"{unical}${code}${gen_code}"
        shifr = code_decoder(natija, l=2)
        otp = Otp.objects.create(mobile=phone, key=shifr, by='login' if key else 'regis', extra=extra)
        request.session['key'] = otp.key
        request.session['code'] = code

        return redirect("otp")  # keyingi darslar

    ctx = {}
    return render(request, "auth/login.html", ctx)


# auth two
def otp(request):
    token = request.session.get("key", None)
    if not token:
        return redirect("auth")

    if request.POST:
        data = request.POST
        code = "".join(data.get(f"otp{x}") for x in range(1, 7))

        otp = Otp.objects.filter(key=token).first()
        if not otp:
            return render(request, "auth/otp.html", {'error': "Token Aniqlanmadi"})

        if otp.is_expired or otp.is_confirmed:
            return render(request, "auth/otp.html", {'error': "Token Allaqachon eskirgan"})

        if not otp.check_date():
            otp.is_expired = True
            otp.save()
            return render(request, "auth/otp.html", {'error': "Tokenning vaqti tugadi"})

        # shifrdan ochish kerak
        natija_code = code_decoder(token, l=2, decode=True).split("$")[1]

        if str(natija_code) != str(code):
            otp.tries += 1
            otp.save()
            return render(request, "auth/otp.html", {'error': f"Xato Kod: {3-otp.tries} urunish qoldi"})

        if otp.by == 'login':
            user = User.objects.filter(phone=otp.mobile).first()
            login(request, user)
        else:
            user = User.objects.create_user(phone=otp.mobile, **otp.extra)
            login(request, user)
            authenticate(request)

        otp.is_expired = otp.is_confirmed = True
        otp.save()
        try:
            del request.session['key']
        except: ...
        return redirect("home")


    return render(request, "auth/otp.html")



def logout(request):
    lout(request)
    return redirect("auth")





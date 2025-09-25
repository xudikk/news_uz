# from methodism.helper import code_decoder, generate_key
import base64
import binascii
import os
import uuid

def generate_key(size=50):
    return binascii.hexlify(os.urandom(size)).decode()


def code_decoder(code, decode=False, l=1):
    if decode:
        for i in range(l):
            code = base64.b64decode(code).decode()
        return code
    else:
        for i in range(l):
            code = base64.b64encode(str(code).encode()).decode()
        return code

code = 986572
unical = uuid.uuid4()  # uzun token hosil qiladi
gen_code = generate_key(15)

natija = f"{unical}${code}${gen_code}"
shifr = code_decoder(natija, l=2)

print(shifr)


# print(unical)
# suz = "salom"

# print(code_decoder(suz, l=2))




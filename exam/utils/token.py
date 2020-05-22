import time

from config.default import *
from .encryption import AESCipher, salt


def become_token(username):
    aes = AESCipher(KEY_SECRET.encode())
    expire_time = int(time.time()) + COOKIE_AGE
    plain_text = '%s|%s|%s' % (str(expire_time), username, salt())
    token = aes.encrypt(plain_text)
    return token
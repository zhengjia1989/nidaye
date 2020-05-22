# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community Edition) available.
Copyright (C) 2017-2018 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

登录态加密方法.

使用AES算法，ECB模式
""" # noqa

from __future__ import unicode_literals
import hashlib
import random
import time
from base64 import urlsafe_b64encode, urlsafe_b64decode

from Crypto.Cipher import AES

import base64
import sys

from Crypto import Random
from Crypto.Cipher import AES
# from django.conf import settings


def salt(length=8):
    """
    生成长度为length 的随机字符串
    """
    aplhabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(map(lambda _: random.choice(aplhabet), range(length)))


class AESCipher:

    def __init__(self, key, iv=Random.new().read(AES.block_size)):
        self.key = key  # key必须是16位 utf8编码
        self.iv = iv  # iv必须是16位 utf8编码
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        text1 = self.__pad(text)
        cipher_text = cipher.encrypt(text1.encode())
        encrypted_str = str(base64.b64encode(cipher_text), encoding='utf-8')
        return encrypted_str

    def decrypt(self, text):
        base_text = base64.b64decode(text)
        cipher = AES.new(self.key, self.mode, self.iv)
        plain_text = cipher.decrypt(base_text).decode('utf-8')
        return self.__unpad(plain_text)

    @staticmethod
    def __pad(text):
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    @staticmethod
    def __unpad(text):
        pad = ord(text[-1])
        return text[:-pad]

    @staticmethod
    def test(key, text):
        cipher = AESCipher(key)
        encrypted_msg = cipher.encrypt(text)
        print(encrypted_msg)
        msg = cipher.decrypt(encrypted_msg)
        print(msg)


if __name__ == '__main__':
    expire_time = str(int(time.time())+70)
    i = 0
    while True:
        time.sleep(1)
        if i > 30:
            break
        AESCipher.test('argt2&_u9upqa4uo'.encode(), '%s|%s|%s' % (expire_time, 'yangxin', salt()))
        now_time = int(time.time())
        if int(expire_time) > now_time:
            print('token有效')
        else:
            print('token无效')
        i += 1
    print(salt())

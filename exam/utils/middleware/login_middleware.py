# -*- coding: utf-8 -*-
import logging

from django.shortcuts import redirect
from django.urls import reverse

try:
    from django.utils.deprecation import MiddlewareMixin
except Exception:
    MiddlewareMixin = object

logger = logging.getLogger('app')


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view, args, kwargs):
        """
        Login paas by two ways
        1. views decorated with 'login_exempt' keyword
        2. User has logged in calling auth.login
        """
        if getattr(view, 'login_exempt', False):
            # 判断该视图是否需要登录
            return None
        if 'e_uid' in request.COOKIES and 'e_username' in request.COOKIES:
            # 验证用户是否登录过, token 是否过期
            uid = request.COOKIES.get('e_uid')
            username = request.COOKIES.get('e_username')
            sessionId = request.COOKIES.get('sessionId')
            s_uid = request.session.get('e_uid')
            s_username = request.session.get('e_username')
            s_sessionId = request.session.get('sessionId')
            logger.info('%s用户登录进来' % username)
            if (int(uid), username, sessionId) == (s_uid, s_username, s_sessionId):
                return None

        # 保存登录前的访问路径

        http_referer = request.scheme + '://' + request.get_host() + request.path
        url = reverse('tologin')
        resp = redirect(url)
        if 'exam' in http_referer.split('/'):
            resp.set_cookie('http_referer', http_referer, max_age=120)
        return resp

    def process_response(self, request, response):
        return response

import json
import random
import uuid
from datetime import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from config.default import *
from exam.models import ExamResult, User, ExamSort, Questions, TestRecord, TestOptions
from .forms import UserInfoForm, RegisterForm

# Create your views here.
# 主页
# from django.urls import reverse
import logging
from .utils.decorators import login_exempt
logger = logging.getLogger('app')


# 登录
@login_exempt
def tologin(request):

    logger.info('%s：访问登录接口' % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    if request.method == 'GET':
        form = UserInfoForm()
        resp = render(request, 'exam/login.html', locals())
        return resp
    else:
        form = UserInfoForm(request.POST)
        if form.is_valid():
            user = User.query(**form.cleaned_data, status=User.STATUS_NORMAL)
            if user:
                user = user.first()
                # 登陆成功即可获取当前登录用户，返回主页/或来源地址
                if request.COOKIES.get('http_referer'):
                    url = request.COOKIES.get('http_referer')
                    resp = redirect(url)
                    resp.delete_cookie('http_referer')
                else:
                    url = reverse('index')
                    resp = redirect(url)
                username = user.username
                sessionid = uid = uuid.uuid4().hex  # 生成浏览器标识
                # 保存cookie
                resp.set_cookie('e_username', username, max_age=COOKIE_AGE)
                resp.set_cookie('sessionId', sessionid, max_age=COOKIE_AGE)
                resp.set_cookie('e_uid', user.id, max_age=COOKIE_AGE)
                # 保存session
                request.session['e_username'] = username
                request.session['e_uid'] = user.id
                request.session['sessionId'] = sessionid
                return resp
            else:
                resp = {
                    'code': 404,
                    'msg': '账号密码不对, 请重新登录'
                }
                return render(request, 'exam/login.html', locals())
        else:
            return render(request, 'exam/login.html', locals())


# 注册
@login_exempt
def register(request):
    if request.method == 'GET':
        form = RegisterForm
        return render(request, 'exam/register.html', locals())
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 注册成功，创建用户
            user = User.objects.create(**form.cleaned_data)
            # 重定向到登录页面
            url = reverse('tologin')  # 反向解析
            return redirect(url)
        else:
            return render(request, 'exam/register.html', locals())


# 退出
def logout_views(request):
    if request.method == 'GET':
        url = reverse('index')
        resp = redirect(url)
        resp.delete_cookie('e_username')
        resp.delete_cookie('e_uid')
        resp.delete_cookie('sessionId')
        del request.session['e_uid']
        del request.session['e_username']
        del request.session['sessionId']
        return resp


# 首页
def index(request):
    if request.method == 'GET':
        uid = request.session.get('e_uid')
        user = User.query(id=uid, status=User.STATUS_NORMAL)
        if user:
            user = user.first()
            records = user.user_results.filter(status=ExamResult.STATUS_NORMAL).order_by('-id')
            if len(records) >= 11:
                height = ''
            else:
                height = 430

            context = {
                'records': records,
                'height': height,
            }
            return render(request, 'exam/index.html', context=context)
        else:
            return render(request, '403.html')


# 考试卷子列表
def test_list_views(request):
    if request.method == 'GET':
        context = {
            'exams': ExamSort.get_query(status=ExamSort.STATUS_NORMAL),
        }
        return render(request, 'exam/exam_list.html', context=context)


# 开始考试
def start_test_views(request, exam_sort_id):
    if request.method == 'GET':
        start = request.GET.get('start')
        end = request.GET.get("end")
        questionNum = request.GET.get('questionNum')
        if all([start, end]):
            start = int(start)
            end = int(end)
            start = start - 1 if start != 0 else start
            end = end - 1 if end != 0 else end
            questions = Questions.get_query(title_id=exam_sort_id).reverse()[start: end]
        elif questionNum:
            questionNum = int(questionNum)
            sample = random.sample(range(Questions.get_query(title_id=exam_sort_id).count()), questionNum)
            questions = [Questions.get_query(title_id=exam_sort_id)[i] for i in sample]
        else:
            sample = random.sample(range(Questions.get_query(title_id=exam_sort_id).count()), 100)
            questions = [Questions.get_query(title_id=exam_sort_id)[i] for i in sample]
        result = ExamResult.exam_create(
                                        user_id=request.user.id,
                                        # user_id=1,
                                        title_id=exam_sort_id,
                                        start_test_time=datetime.now(),
                                        )
        for question in questions:
            TestRecord.test_record_create(question_id=question.id, exam_result_id=result.id)
        url = reverse('page', args=(result.id, 1, 0))
        return redirect(url)


# 分页处理
def page_view(request, result_id, page_index, status):
    qestions_all = TestRecord.get_query(exam_result_id=result_id)
    paginator = Paginator(qestions_all, 10)  # 实例化Paginator, 每页显示10条数据
    page = paginator.page(page_index)  # 传递当前页的实例对象到前端
    if int(status):
        lst = []
        for record in page:
            opts = record.question.question_options.filter(status=TestOptions.STATUS_NORMAL)
            for opt in opts:
                if opt.desc.split('.')[0] in record.answer:
                    lst.append(opt.id)
        context = {
            'page': page,
            'lst': lst,
            'result_id': result_id,
        }
        # 去考试记录
        return render(request, 'exam/test_record.html', context=context)
    else:
        # 去考试
        context = {"page": page, 'result_id': result_id}
        return render(request, "exam/exam_detail.html", context)


# 考试结果
def test_result_views(request):
    if request.method == 'POST':
        result_id = request.POST.get('result_id')
        options = request.POST.get('options')
        options = json.loads(options)
        print(options)
        if not all([result_id, options]):
            return JsonResponse({'code': 401, 'msg': '缺少参数'})
        score = 0
        for key in options:
            record_id = key.get('test_record_id')
            # 获取问题记录
            test_record = TestRecord.get_query(id=record_id).first()
            lst = []
            # 获取答案
            for opt_id in key.get('opts'):
                opt = TestOptions.get_query(id=opt_id, status=TestOptions.STATUS_NORMAL)
                if opt:
                    opt = opt.first()
                    lst.append(opt.desc.split('.')[0])
            if not lst:
                continue
            answer = ','.join(lst)
            test_record.answer = answer
            test_record.save()
            if answer == test_record.question.standard_answer:
                score += 1
        result = ExamResult.get_query(id=result_id).first()
        result.score = score
        if 90 <= score <= 100:
            result.score_rank = ExamResult.RANK_EXCELLENT
        elif 80 <= score < 90:
            result.score_rank = ExamResult.RANK_WELL
        elif 60 <= score < 80:
            result.score_rank = ExamResult.RANK_PASS
        else:
            result.score_rank = ExamResult.RANK_FAIL
        result.end_test_time = datetime.now()
        result.save()
        url = reverse('test_detail', args=(result.id,))
        return redirect(url)


# 考试详情
def test_detail_views(request, result_id):
    context = {
        'result': ExamResult.get_query(id=result_id).first(),
    }
    return render(request, 'exam/test_result.html', context=context)



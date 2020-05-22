from django.test import TestCase

# Create your tests here.
import re
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")  # 设置环境变量
import django
django.setup()
from exam.models import ExamSort, Questions, TestOptions

reg1 = re.compile(r'(^运维自动化工程师\(BKOS\)理论基础)', re.I)
# reg1 = re.compile(r'(^运维开发工程师\(BKDS\)理论基础)', re.I)
reg2 = re.compile(r'\*#\*(\d+\..*?)\*#\*', re.S)
reg3 = re.compile(r'正确答案：(.*)')
reg4 = re.compile(r'\*#\*\s+(.*?)正确答案', re.S)

text_path = '3.txt'
with open(text_path, 'r', encoding='utf-8') as f:
    res = f.read()
    res1 = reg1.findall(res)
    res2 = reg2.findall(res)
    # for k in reg2.findall(res):
    #     print(k)

    res3 = reg3.findall(res)
    # for k in reg3.findall(res):
    #     print(k)
    #
    res4 = reg4.findall(res)
    # for k in reg4.findall(res):
    #     print(k)

    for title in res1:
        exam_sort = ExamSort()
        exam_sort.title = title.strip()
        exam_sort.save()
        for question, answer, opts in zip(res2, res3, res4):
            exam_question = Questions()
            exam_question.title_id = exam_sort.id
            exam_question.question = question.strip()
            exam_question.standard_answer = answer.strip()
            if len(answer.split(',')) > 1:
                exam_question.choice_status = 1
            else:
                exam_question.choice_status = 0
            exam_question.save()
            options = opts.split('\n')
            print(options)
            for choice in options:
                if choice.strip():
                    test_option = TestOptions()
                    test_option.desc = choice.strip()
                    test_option.question_id = exam_question.id
                    test_option.save()
# ExamSort.objects.get(id=3).delete()






from django.db import models
from datetime import datetime

# Create your models here.


class User(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0

    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    username = models.CharField(max_length=30, default='', verbose_name='账号')
    password = models.CharField(max_length=30, default='', verbose_name='密码')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")

    class Meta:
        db_table = "user"
        verbose_name = verbose_name_plural = '用户表'

    def __str__(self):
        return self.username

    @classmethod
    def query(cls, **kwargs):
        return cls.objects.filter(**kwargs)


class ExamSort(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0

    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    title = models.CharField(max_length=100, default='', verbose_name='卷子题目')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    created_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")

    class Meta:
        db_table = "exam_sort"
        verbose_name = verbose_name_plural = "卷子"

    def __str__(self):
        return self.title

    @classmethod
    def get_query(cls, **kwargs):
        return cls.objects.filter(**kwargs).order_by('-id')


class Questions(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0

    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    CHOICE_ONE = 0
    CHOICE_MULTIPLE = 1
    CHOICE_ITEMS = (
        (CHOICE_ONE, '单选'),
        (CHOICE_MULTIPLE, '多选'),
    )
    title = models.ForeignKey(ExamSort, default='', related_name='exam_title',
                              on_delete=models.CASCADE, verbose_name='考试题目')
    question = models.CharField(max_length=1024, default='', verbose_name='问题')
    standard_answer = models.CharField(max_length=20, default='', verbose_name='标准答案', help_text='多个答案以逗号分隔')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    choice_status = models.PositiveIntegerField(default=CHOICE_ONE, choices=CHOICE_ITEMS, verbose_name="选题类型")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "questions"
        verbose_name = verbose_name_plural = "试题库"
        # 根据id进行降序排列
        ordering = ["-id"]

    def __str__(self):
        return self.question

    @classmethod
    def get_query(cls, **kwargs):
        return cls.objects.filter(**kwargs)


class TestOptions(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0

    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    desc = models.CharField(max_length=1024, default='', verbose_name='选项')
    question = models.ForeignKey(Questions, default='', related_name='question_options',
                                 on_delete=models.CASCADE, verbose_name='题目')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "test_options"
        verbose_name = verbose_name_plural = "试题选项"

    def __str__(self):
        return self.desc

    @classmethod
    def get_query(cls, **kwargs):
        return cls.objects.filter(**kwargs)


class ExamResult(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    RANK_EXCELLENT = 0
    RANK_WELL = 1
    RANK_PASS = 2
    RANK_FAIL = 3
    RANK_ITEM = (
        (RANK_EXCELLENT, '优秀'),
        (RANK_WELL, '良好'),
        (RANK_PASS, '及格'),
        (RANK_FAIL, '不及格'),
    )

    user = models.ForeignKey(User, default='', related_name='user_results',
                             on_delete=models.CASCADE, verbose_name='考生')
    title = models.ForeignKey(ExamSort, default='', related_name='title_results',
                              on_delete=models.CASCADE, verbose_name='考试题目')
    score = models.IntegerField(default=0, verbose_name='分数')
    score_rank = models.PositiveIntegerField(default=RANK_FAIL, choices=RANK_ITEM, verbose_name='成绩等级')
    start_test_time = models.DateTimeField(null=True, verbose_name='考试开始时间')
    end_test_time = models.DateTimeField(null=True, verbose_name='考试结束时间')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "exam_result"
        verbose_name = verbose_name_plural = "考试结果"

    def __str__(self):
        return self.user.username

    @classmethod
    def get_query(cls, **kwargs):
        return cls.objects.filter(status=cls.STATUS_NORMAL, **kwargs)

    @classmethod
    def exam_create(cls, **kwargs):
        return cls.objects.create(**kwargs)


class TestRecord(models.Model):
    question = models.ForeignKey(Questions, default='', related_name='questions_record',
                                 on_delete=models.CASCADE, verbose_name='题目')
    answer = models.CharField(max_length=20, default='', verbose_name='答案')
    exam_result = models.ForeignKey(ExamResult, default='', related_name='result_test_record',
                                    on_delete=models.CASCADE, verbose_name='考试结果')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "test_record"
        verbose_name = verbose_name_plural = "考试记录"
        ordering = ['id']

    def __str__(self):
        return self.question.question

    @classmethod
    def test_record_create(cls, **kwargs):
        cls.objects.create(**kwargs)

    @classmethod
    def get_query(cls, **kwargs):
        return cls.objects.filter(**kwargs)
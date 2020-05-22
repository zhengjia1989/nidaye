from django.urls import re_path
from .views import (tologin, register, logout_views, index, test_list_views, start_test_views,
                    test_result_views, page_view, test_detail_views)


urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^login/$', tologin, name='tologin'),
    re_path(r'^register/$', register, name='register'),
    re_path(r'^logout/$', logout_views, name='logout'),
    re_path(r'^test_list/$', test_list_views, name='test_list'),
    re_path(r'^start_test/(?P<exam_sort_id>\d+)/$', start_test_views, name='start_test'),
    re_path(r'^test_result/$', test_result_views, name='test_result'),
    re_path(r'^page/(?P<result_id>\d+)/(?P<page_index>\d+)/(?P<status>\d+)/$', page_view, name='page'),
    re_path(r'^test_detail/(?P<result_id>\d+)/$', test_detail_views, name='test_detail'),
]
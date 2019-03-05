from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_date, get_tody_hot_data, get_yesterday_hot_data, get_7_days_hot_data
from blog.models import Blog


def get_7_days_hot_blogs():
    pass


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_date(blog_content_type)
    today_hot_data = get_tody_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
    hot_data_7_days = get_7_days_hot_data(blog_content_type)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['hot_data_7_days'] = hot_data_7_days
    return render(request, 'home.html', context)

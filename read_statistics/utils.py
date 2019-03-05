import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from .models import ReadNum, ReadDetail

# 统计访问计数


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '{}_{}_read'.format(ct.model, obj.pk)

    if not request.COOKIES.get(key):

        # if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
        #     # 存在记录
        #     readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        # else:
        #     # 不存在对应记录
        #     readnum = ReadNum(content_type=ct, object_id=obj.pk)
        # django提供的方法，存在就找到，不存在就创建
        # 总阅读数加 +1
        readnum, created = ReadNum.objects.get_or_create(
            content_type=ct, object_id=obj.pk)
        # 计数加1
        readnum.read_num += 1
        readnum.save()

        date = timezone.now().date()
        # if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date).count():
        #     readDetail = ReadDetail.objects.get(
        #         content_type=ct, object_id=obj.pk, date=date)
        # else:
        #     readDetail = ReadDetail(
        #         content_type=ct, object_id=obj.pk, date=date)
        # 当天阅读数 +1
        readDetail, created = ReadDetail.objects.get_or_create(
            content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key

# 获取前七日访问量


def get_seven_days_read_date(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(
            content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums


# 今日热门博客


def get_tody_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(
        content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7]  # limit 7 取前7条

# 昨日热门博客


def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(
        content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:7]


def get_7_days_hot_data(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    read_details = ReadDetail.objects.filter(content_type=content_type, date__lt=today, date__gte=date).values(
        'content_type', 'object_id').annotate(Sum(read_num_sum='read_num')).order_by('-read_num')

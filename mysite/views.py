import datetime
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.models import User

from read_statistics.utils import get_seven_days_read_date, get_tody_hot_data, get_yesterday_hot_data
from blog.models import Blog
from .forms import LoginForm, RegForm


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date).values(
        'id', 'title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return blogs[:7]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_date(blog_content_type)

    # 获取7天热门博客的缓存是数据
    hot_blogs_7_days = cache.get('hot_blogs_7_days')
    if hot_blogs_7_days is None:
        hot_blogs_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_7_days', hot_blogs_7_days, 3600)
    #     print('calc')
    # else:
    #     print('use cache')
    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_tody_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_blogs_7_days'] = get_7_days_hot_blogs()
    return render(request, 'home.html', context)


@csrf_exempt
def login(request):
    # username = request.POST.get('username', '')
    # password = request.POST.get('password', '')
    # user = auth.authenticate(request, username=username, password=password)
    # referer = request.META.get('HTTP_REFERER', reverse('home'))

    # if user is not None:
    #     auth.login(request, user)
    #     return redirect(referer)
    # else:
    #     return render(request, 'error.html', {'message': '用户名或密码不正确'})
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            # 还可以使用下面的方式创建用户
            # user = User()
            # user.username = username
            # user.email = email
            # user.set_password = password
            # user.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)

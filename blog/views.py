from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
# from django.contrib.contenttypes.models import ContentType

from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read
# from comment.models import Comment
# from comment.forms import CommentForm


# 获取博客列表共同数据，分页


def get_blog_list_data(request, blogs_all_list):
    page_num = request.GET.get('page', 1)
    # 每5页进行分页
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)
    # 总页数
    page_of_blogs = paginator.get_page(page_num)
    # 获取当前页
    current_page_num = page_of_blogs.number
    # 获取当前页面前后各两页，去掉小于1和大与最大页的
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
        range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上省略标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取博客分类的对应博客数量
    # BlogType.objects.annotate(blog_count=Count('blog'))
    # blog_types = BlogType.objects.all()
    # blog_type_list = []
    # for blog_type in blog_types:
    #     blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
    #     blog_types_list.append(blog_ytpe)

    # 获取日期归档对博客数量
    blog_dates = Blog.objects.dates(
        'created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(
            created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    # context['blog_types'] = blog_type_list
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    # context['blog_dates'] = Blog.objects.dates(
    #    'created_time', 'month', order='DESC')
    context['blog_dates'] = blog_dates_dict
    return context

# 博客列表


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)

# 博客详情页


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)
    # blog_content_type = ContentType.objects.get_for_model(blog)
    # comments = Comment.objects.filter(
    #    content_type=blog_content_type, object_id=blog.pk, parent=None)

    context = {}
    context['blog'] = blog
    context['user'] = request.user
    # context['comments'] = comments.order_by('-comment_time')
    # data = {}
    # data['content_type'] = blog_content_type.model
    # data['object_id'] = blog_pk
    # data['reply_comment_id'] = 0
    # context['comment_form'] = CommentForm(initial=data)

    # 上一条博客
    context['previous_blog'] = Blog.objects.filter(
        created_time__gt=blog.created_time).last()

    # 下一条博客
    context['next_blog'] = Blog.objects.filter(
        created_time__lt=blog.created_time).first()

    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记
    return response

# 博客类型


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_data(request, blogs_all_list)
    context['blog'] = blog_type
    response = render(request, 'blog/blogs_with_type.html', context)
    return response

# 时间归档


def blog_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(
        created_time__year=year, created_time__month=month)
    context = get_blog_list_data(request, blogs_all_list)
    context['blog_with_date'] = "{}年{}月".format(year, month)
    print(context['blog_with_date'])
    return render(request, 'blog/blog_with_date.html', context)

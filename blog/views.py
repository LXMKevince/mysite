from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator
from django.conf import settings


# 获取博客列表共同数据


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

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates(
        'created_time', 'month', order='DESC')
    return context

# 博客列表


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)

# 博客详情页


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    context['blog'] = blog
    # 上一条博客
    context['previous_blog'] = Blog.objects.filter(
        created_time__gt=blog.created_time).last()
    # 下一条博客
    context['next_blog'] = Blog.objects.filter(
        created_time__lt=blog.created_time).first()
    return render(request, 'blog/blog_detail.html', context)

# 博客类型


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_data(request, blogs_all_list)
    context['blog'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)

# 时间归档


def blog_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(
        created_time__year=year, created_time__month=month)
    context = get_blog_list_data(request, blogs_all_list)
    context['blog_with_date'] = "{}年{}月".format(year, month)
    print(context['blog_with_date'])
    return render(request, 'blog/blog_with_date.html', context)

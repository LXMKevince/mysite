from django.urls import path
from . import views


urlpatterns = [
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
]

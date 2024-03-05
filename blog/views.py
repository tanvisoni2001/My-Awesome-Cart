from django.shortcuts import render
from django.http import HttpResponse
from .models import BlogPost

# Create your views here.

def index(request):
    posts = BlogPost.objects.all 

    return render(request, 'blog/index.html', {'posts': posts})


def blogPost(request,id):
    post = BlogPost.objects.filter(post_id = id)
    return render(request, 'blog/blogPost.html', {'post':post[0]})
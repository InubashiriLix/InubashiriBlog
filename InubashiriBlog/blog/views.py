from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Q, F
from django.http import HttpResponse
from django.http import JsonResponse

from .models import BlogCategory, BlogComment, Blog
from .forms import PubBlogForm
from blog_auth.models import AvatarModel

from snakes.get_base_context import get_base_context


def get_blog_content_with_avatar(blogs_content: list) -> list:
    blogs = []
    for blog in blogs_content:
        avatar = AvatarModel.objects.filter(user_id=blog.author_id).last()
        if avatar:
            blogs.append({"blog": blog, "avatar": avatar.image.url})
        else:
            blogs.append({"blog": blog, "avatar": None})
    return blogs


def index(request):
    base_context = get_base_context(request=request)
    q = "【MAIN】"
    # the content in the index' searching
    blogs_contents = Blog.objects.filter(Q(title__icontains="【!!!】") | Q(title__icontains="【!!】") | Q(title__icontains='【RULE】') | Q(title__icontains=q)).all()
    blogs: list = get_blog_content_with_avatar(blogs_content=blogs_contents)
    return render(request, 'index.html', context=base_context | {"blogs": blogs})


def detail_blog(request, blog_id):
    base_context = get_base_context(request=request)
    try:
        # TODO: 给昵称加上超链接
        blog = Blog.objects.get(id=blog_id)

        author_avatar = AvatarModel.objects.filter(user_id=blog.author_id).last()
        if author_avatar:
            author_avatar_url = author_avatar.image.url
        else:
            author_avatar_url = None

        comments = []
        for comment in blog.comments.all():
            comment_single_avatar = AvatarModel.objects.filter(user_id=comment.author_id).last()
            comment_avatar_url = comment_single_avatar.image.url if comment_single_avatar else None
            comments.append({'comment': comment, 'comment_avatar': comment_avatar_url})

        return render(request, 'blog_detail.html', context=base_context | {'blog': blog,
                                                                           "author_avatar": author_avatar_url,
                                                                           "comments": comments})
    except Exception as e:
        context = {"error": str(e)}
        return render(request, 'error_invalid_blog.html', context=base_context | context)


@require_POST
@login_required()
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    # author = request.user
    # pub_time is auto now in model
    blog_comment = BlogComment.objects.create(blog_id=blog_id, content=content, author=request.user)
    return redirect(reverse('blog:blog_detail', args=[blog_id]))


@require_http_methods(['GET', 'POST'])
@login_required()
def pub_blog(request):
    base_context = get_base_context(request=request)
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, 'pub_blog.html', context=base_context | {'categories': categories})
    else:
        form = PubBlogForm(request.POST)
        # 手动验证每个字段
        if form.is_bound:  # 确保表单已经绑定数据
            for field_name in form.fields:
                field = form[field_name]
                if not field.errors:
                    print(f"{field_name} is valid")
                else:
                    print(f"Error in {field_name}: {field.errors}")
        # 收到表单时打印表单数据
        print(form.data)
        if form.is_valid():

            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            category_id = form.cleaned_data.get('category')
            content = form.cleaned_data.get('content')

            blog = Blog.objects.create(title=title, content=content, category_id=category_id, description=description, author=request.user)
            # return JsonResponse({'code': 200, 'message': 'done', "data": {"blog_id": blog.id}})
            return redirect(reverse("blog:blog_detail", args=[blog.id]))
        else:
            # 如果表单无效，返回用户填写的内容和错误信息
            categories = BlogCategory.objects.all()
            # return HttpResponse('error')
            return render(request, 'pub_blog.html', base_context | {
                'form': form,
                'categories': categories,  # 保证类别选择不丢失
                'error_message': 'There was an error with your submission. Please correct the highlighted fields.',
            })


@require_GET
def search_blog(request):
    base_context = get_base_context(request=request)
    q = request.GET.get('q')
    blogs_contents = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).all()
    blogs = get_blog_content_with_avatar(blogs_content=blogs_contents)
    return render(request, 'search.html', context=base_context | {"blogs": blogs})


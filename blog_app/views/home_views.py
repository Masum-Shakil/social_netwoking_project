from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from authentication_app.models import profile_models
from blog_app.models import post_models
from blog_app.forms import post_forms
from django.contrib import messages
from authentication_app.models import profile_models

@login_required

def index_view(request):
    profile = profile_models.Profile.objects.get(user = request.user)
    posts = post_models.Posts.objects.filter(created_by=request.user).order_by('-created_at')
    post_list = []

    for item in posts:
        temp_list = []
        temp_list.append(item)
        like = post_models.PostLikes.objects.filter(blog_post = item)
        comments = post_models.PostComments.objects.filter(blog_post = item)
        temp_list.append(len(like))
        temp_list.append(len(comments))
        shares = post_models.PostSharings.objects.filter(blog_post = item)
        temp_list.append(len(shares))
        post_list.append(temp_list)

    context = {
        'profile' : profile,
        'posts' : posts,
        'post_list' : post_list
    }

    return render(request, 'blog_app/my_wall.html', context)

@login_required

def create_post_view(request):
    form = post_forms.PostCreateForm()

    if request.method == "POST":
        form = post_forms.PostCreateForm(request.POST, request.FILES)

        if form.is_valid():
            form = form.save(commit=False)
            form.created_by = request.user
            form.save()
            messages.success(request, "Post is created successfully!!")
            return redirect('home')

    context = {
        'form' : form
    }

    return render(request, 'blog_app/post_create.html', context)

@login_required

def like_post(request, id):

    try:
        post_models.PostLikes.objects.create(blog_post_id= id, liked_by=request.user)
        messages.success(request, "Post is liked successfully!!")

    except:
        messages.warning(request, "Sorry you can not like the same post again!!")

    return redirect('home')

@login_required

def comment_post(request, id):
    form = post_forms.CommentCreateForm()
    blog_post = post_models.Posts.objects.get(id=id)
    comments = post_models.PostComments.objects.filter(blog_post=blog_post).order_by('-created_at')
    likes = post_models.PostLikes.objects.filter(blog_post=blog_post)
    shares = post_models.PostSharings.objects.filter(blog_post=blog_post)

    if request.method == 'POST':
        form = post_forms.CommentCreateForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.created_by = request.user
            form.blog_post = blog_post
            form.save()
            messages.success(request, "Comment is added successfully!!")
            return redirect('home')

    context = {
        'form' : form,
        'blog_post' : blog_post,
        'comments' : comments,
        'number_of_comments' : len(comments),
        'number_of_likes' : len(likes),
        'number_of_shares' : len(shares)
    }

    return render(request, 'blog_app/comment_create.html', context)

@login_required

def share_post(request, id):

    try:
        post_models.PostSharings.objects.create(blog_post_id= id, shared_by=request.user)
        messages.success(request, "Post is shared successfully!!")

    except:
        messages.warning(request, "Sorry you can not share the same post again!!")

    return redirect('home')

@login_required

def view_shared_posts(request):
    my_friends_user_id_list = list(profile_models.FriendshipModels.objects.filter(from_friend_request__user = request.user, friend_request_status = 'confirmed').values_list('to_friend_request__user__id', flat=True))
    my_friends_user_id_list.append(request.user.id)
    own_shared_posts = list(post_models.PostSharings.objects.filter(shared_by__id__in=my_friends_user_id_list).values_list('blog_post__id', flat=True))
    posts = post_models.Posts.objects.filter(id__in=own_shared_posts).order_by('-created_at')
    post_list = []

    for item in posts:
        temp_list = []
        temp_list.append(item)
        like = post_models.PostLikes.objects.filter(blog_post = item)
        comments = post_models.PostComments.objects.filter(blog_post = item)
        temp_list.append(len(like))
        temp_list.append(len(comments))
        shares = post_models.PostSharings.objects.filter(blog_post = item)
        temp_list.append(len(shares))
        post_list.append(temp_list)

    context = {
        'posts' : posts,
        'post_list' : post_list
    }

    return render(request, 'blog_app/shared_post.html', context)

@login_required

def my_friends_wall(request):
    my_friends_user_id_list = list(profile_models.FriendshipModels.objects.filter(from_friend_request__user = request.user, friend_request_status = 'confirmed').values_list('to_friend_request__user__id', flat=True))
    my_frinds_posts = post_models.Posts.objects.filter(created_by__id__in = my_friends_user_id_list)
    post_list = []

    for item in my_frinds_posts:
        temp_list = []
        temp_list.append(item)
        like = post_models.PostLikes.objects.filter(blog_post = item)
        comments = post_models.PostComments.objects.filter(blog_post = item)
        temp_list.append(len(like))
        temp_list.append(len(comments))
        shares = post_models.PostSharings.objects.filter(blog_post = item)
        temp_list.append(len(shares))
        post_list.append(temp_list)

    context = {
        'post_list' : post_list
    }

    return render(request, 'blog_app/my_friends_posts.html', context)

@login_required

def search_views(request):
    search_input= request.GET.get('search_input')
    my_friends = list(profile_models.FriendshipModels.objects.filter(from_friend_request__user =request.user, friend_request_status = 'confirmed').values_list('to_friend_request__user__id', flat=True))
    print("Type: ", type(request.user))
    my_friends.append(request.user.id)
    my_frinds_posts = post_models.Posts.objects.filter(post_title__icontains=search_input, created_by__id__in = my_friends) | post_models.Posts.objects.filter(post_details__icontains=search_input, created_by__id__in = my_friends)
    post_list = []

    for item in my_frinds_posts:
        temp_list = []
        temp_list.append(item)
        like = post_models.PostLikes.objects.filter(blog_post = item)
        comments = post_models.PostComments.objects.filter(blog_post = item)
        temp_list.append(len(like))
        temp_list.append(len(comments))
        shares = post_models.PostSharings.objects.filter(blog_post = item)
        temp_list.append(len(shares))
        post_list.append(temp_list)

    context = {
        'post_list' : post_list
    }

    return render(request, 'blog_app/search_posts.html', context)
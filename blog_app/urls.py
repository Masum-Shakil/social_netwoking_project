from django.urls import path
from blog_app.views import home_views

urlpatterns = [
    path('',home_views.index_view, name='home'),
    path('create_post',home_views.create_post_view, name='create_post'),
    path('like_post/<int:id>',home_views.like_post, name='like_post'),
    path('comment_post/<int:id>',home_views.comment_post, name='comment_post'),
    path('share_post/<int:id>',home_views.share_post, name='share_post'),
    path('view_shared_posts',home_views.view_shared_posts, name='view_shared_posts'),
    path('my_friend_posts',home_views.my_friends_wall, name='my_friend_posts'),
    path('search',home_views.search_views, name='searching')
]
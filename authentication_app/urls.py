from django.urls import path
from authentication_app.views import credential_views, profile_update_views, friends_views

urlpatterns = [
    path('', credential_views.login_view, name='login'),
    path('signup/', credential_views.sign_up_view, name='signup'),
    path('profile/update', profile_update_views.profile_update_view, name='profile_update'),
    path('logout', credential_views.custom_logout, name='custom_logout'),
    path('friends', friends_views.my_friends_view, name='friends_views'),
    path('friend/request/send/<int:id>', friends_views.send_friend_request_view, name='send_friend_request'),
    path('accept/friend/request/<int:id>', friends_views.accept_friend_request, name='accept_friend_request'),
    path('cancel/friend/request/<int:id>', friends_views.cancel_friend_request, name='cancel_friend_request'),
    path('unfriend/<int:id>', friends_views.unfriend_view, name='unfriend')
]
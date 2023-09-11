from authentication_app.models import profile_models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required

def my_friends_view(request):
    my_friends = profile_models.FriendshipModels.objects.filter(from_friend_request__user =request.user, friend_request_status = 'confirmed')
    friend_request = profile_models.FriendshipModels.objects.filter(to_friend_request__user =request.user, friend_request_status = 'pending')
    friend_request_list = list(profile_models.FriendshipModels.objects.filter(to_friend_request__user =request.user, friend_request_status = 'pending').values_list('from_friend_request__id', flat=True))
    my_friends_list = list(profile_models.FriendshipModels.objects.filter(from_friend_request__user=request.user, friend_request_status = 'confirmed').values_list('to_friend_request__id', flat=True))
    people_you_may_know = profile_models.Profile.objects.all().exclude(user=request.user).exclude(id__in=my_friends_list).exclude(id__in=friend_request_list)

    context = {
        'my_friends' : my_friends,
        'people_you_may_know' : people_you_may_know,
        'friend_request' : friend_request
    }

    return render(request, 'authentication_app/my_friends.html', context)

@login_required

def send_friend_request_view(request, id):
    my_user = profile_models.Profile.objects.get(user=request.user)

    try:
        profile_models.FriendshipModels.objects.create(from_friend_request=my_user, to_friend_request_id=id, friend_request_status='pending')
        messages.success(request, "Friend request is sent!!")

    except:
        messages.warning(request, "Sorry you can not send friend request to same user twice!!")

    return redirect("friends_views")

@login_required

def accept_friend_request(request,id):
    my_user = profile_models.Profile.objects.get(user=request.user)
    from_friend = profile_models.FriendshipModels.objects.get(from_friend_request__id=id, to_friend_request=my_user, friend_request_status='pending')
    from_friend.friend_request_status = 'confirmed'
    from_friend.save()
    profile_models.FriendshipModels.objects.create(from_friend_request=my_user, to_friend_request_id = from_friend.from_friend_request.id, friend_request_status = 'confirmed')
    messages.success(request, "Accepted the friend request successfully!!")
    return redirect("friends_views")

@login_required

def cancel_friend_request(request,id):
    cancel_friend_request = profile_models.FriendshipModels.objects.get(id=id)
    cancel_friend_request.delete()
    messages.success(request, "Friend request is cancelled!!")
    return redirect("friends_views")

@login_required

def unfriend_view(request, id):
    unfriend = profile_models.FriendshipModels.objects.get(id=id)
    reverse_relation=profile_models.FriendshipModels.objects.get(from_friend_request_id=unfriend.to_friend_request.id, to_friend_request_id=unfriend.from_friend_request.id, friend_request_status='confirmed')
    reverse_relation.delete()
    unfriend.delete()
    messages.success(request, "Unfriend is successfull!!")
    return redirect("friends_views")
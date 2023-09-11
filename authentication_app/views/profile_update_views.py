from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication_app.models import profile_models
from authentication_app.forms import profile_update_form
from django.contrib import messages

@login_required

def profile_update_view(request):
    profile = profile_models.Profile.objects.get(user=request.user)
    form = profile_update_form.ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        form = profile_update_form.ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile is updated!!!")
            return redirect('home')

    context = {
        'form' : form
    }

    return render(request, 'authentication_app/profile_update.html', context)
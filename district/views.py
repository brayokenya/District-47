from django.http  import HttpResponse
from django.shortcuts import render,redirect
import datetime as dt
from django.http  import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout



# Create your views here.
def index(request):
    return render(request, 'index.html')

# User Register 
def register(request):
    registered = False
    

    if request.method == "POST":
        user_form = UserForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_profile = UserProfile()
            user_profile.user = user
            # user_profile.save()
            user_profile.save()
            registered = True
            

            return HttpResponseRedirect(reverse("user_login"))

        else:
            pass

    else:
        user_form = UserForm()
        

    return render(request, "auth/register.html", context={"user_form":user_form,
                                                          "registered":registered})
# User Login view
def user_login(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:
                login(request, user)

                return HttpResponseRedirect(reverse("dist"))
            else:
                return HttpResponseRedirect(reverse("user_login")) #raise error/ flash

        else:
            return HttpResponseRedirect(reverse("user_login")) #raise error/ flash
    else:
        return render(request, "auth/login.html", context={})

#User Logout View
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("dist"))

@login_required
def profile(request, id):
    user = User.objects.get(id=id)
    profile = UserProfile.objects.get(user_id=user)
    sites = Site.objects.filter(profile__id=id)[::-1]
    return render(request, "websites/profile.html", context={"user":user,
                                                             "profile":profile,
                                                             "sites":sites})
@login_required(login_url='/accounts/login/')
def create_profile(request):
    current_user_id = request.user.id
    user_profile = UserProfile.objects.get(user_id=current_user_id)
    if request.method == 'POST':

        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid(): 

            user_profile.profile_pic = form.cleaned_data.get('profile_pic')
            user_profile.phone_number = form.cleaned_data.get('phone_number')
            user_profile.bio = form.cleaned_data.get('bio')

            user_profile.save()
            messages.success(request, 'Your profile has been updated.')
        return redirect(my_profile)

    else:
        form = UserProfileForm()
    return render(request, 'create-profile.html', {"form": form})



@login_required(login_url='/accounts/login/')
def my_profile(request):
    current_user_id = request.user.id
    user_profile = UserProfile.objects.get(user_id=current_user_id)
    
    try:
        profile = UserProfile.objects.get(user_id=current_user_id)
    except UserProfile.DoesNotExist:
        return redirect(create_profile)
    site = Site.objects.filter(developer_id=current_user_id)
    

    return render(request, 'my-profile.html', { "site": site, "user_profile": user_profile},)
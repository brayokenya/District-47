from django.http  import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
import datetime as dt
from django.http  import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout



# Create your views here.
@login_required
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
    hoods = NeighbourHood.objects.filter(profile__id=id)[::-1]
    return render(request, "websites/profile.html", context={"user":user,
                                                             "profile":profile,
                                                            "hoods":hoods})

#Create Profile View
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


#user profile view
@login_required(login_url='/accounts/login/')
def my_profile(request):
    current_user_id = request.user.id
    user_profile = UserProfile.objects.get(user_id=current_user_id)
    
    try:
        profile = UserProfile.objects.get(user_id=current_user_id)
    except UserProfile.DoesNotExist:
        return redirect(create_profile)
    hood = NeighbourHood.objects.filter(admin_id=current_user_id)
    

    return render(request, 'my-profile.html', { "hood": hood, "user_profile": user_profile},)


###################################################################

def hoods(request):
    all_hoods = NeighbourHood.objects.all()
    all_hoods = all_hoods[::-1]
    params = {
        'all_hoods': all_hoods,
    }
    return render(request, 'all_hoods.html', params)


def create_hood(request):
    if request.method == 'POST':
        form = NeighbourHoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.admin = request.user.profile
            hood.save()
            return redirect('hood')
    else:
        form = NeighbourHoodForm()
    return render(request, 'newhood.html', {'form': form})


def single_hood(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    business = Business.objects.filter(neighbourhood=hood)
    posts = Post.objects.filter(hood=hood)
    posts = posts[::-1]
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            b_form = form.save(commit=False)
            b_form.neighbourhood = hood
            b_form.user = request.user.profile
            b_form.save()
            return redirect('single-hood', hood.id)
    else:
        form = BusinessForm()
    params = {
        'hood': hood,
        'business': business,
        'form': form,
        'posts': posts
    }
    return render(request, 'single_hood.html', params)


def hood_members(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    members = Profile.objects.filter(neighbourhood=hood)
    return render(request, 'members.html', {'members': members})


def create_post(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.hood = hood
            post.user = request.user.profile
            post.save()
            return redirect('single-hood', hood.id)
    else:
        form = PostForm()
    return render(request, 'post.html', {'form': form})


def join_hood(request, id):
    neighbourhood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = neighbourhood
    request.user.profile.save()
    return redirect('hood')


def leave_hood(request, id):
    hood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = None
    request.user.profile.save()
    return redirect('hood')

def search_business(request):
    if request.method == 'GET':
        name = request.GET.get("title")
        results = Business.objects.filter(name__icontains=name).all()
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'results.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, "results.html")
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime



#CLIENT SIDE COOKIE METHOD
# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# Updated the function definition
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1
#update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())

    else:
# set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
# Update/set the visits cookie
    request.session['visits'] = visits

def index(request):
    #request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    visitor_cookie_handler(request)
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    context_dict = {'categories': category_list, 'pages': page_list, 'visits':visits}
    response = render(request, 'rango/index.html', context=context_dict)
    return response

# If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
#update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now()) 
    else:
# set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
# Update/set the visits cookie
        request.session['visits'] = visits   

def about(request):
    #visitor_cookie_handler(request)
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    
    context_dict = {'boldmessage':'ABOUT MY FRUITS', 'MEDIA_URL':'/media/','visits':visits}
    
    return render(request, 'rango/about.html', context=context_dict) #

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html',{'form':form})

@login_required
def add_page(request,category_name_slug):
    #get the category name if it exists, this category name is specified by the url submitted
    try:
        category = Category.objects.get(slug=category_name_slug) #assign 'category' to the result of 'can you find the category_name_slug from Category objects
    except Category.DoesNotExist: #if the result of the search was Category.DoesNotExist then category = None
        category = None

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False) #do not commit it to the page model yet
                page.category = category 
                page.views = 0
                page.save()
                return show_category(request,category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form':form, 'category':category}
    return render(request, 'rango/add_page.html',context_dict)
    
@login_required
def user_profile(request):

    return render(request, 'registration/profile.html',{})

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            
            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request,'rango/register.html',
    {'user_form':user_form,'profile_form':profile_form,'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('rango:index'))
            else:
                return HttpResponseRedirect("YOUR FRUIT ACCOUNT IS DISABLED")
        else:
            if User.objects.filter(username=username).exists():
                return HttpResponse("INVALID PASSWORD")
            else:
                return HttpResponse("INVALID USERNAME AND/OR PASSWORD")
    else:
        return render(request, 'rango/login.html',{}) #ensure it is rendered if the request is a GET (not POST)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('rango:index'))

@login_required
def restricted(request):

    return HttpResponseRedirect(reverse('rango:restricted'))

def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass
        
    return redirect(url)

@login_required
def register_profile(request):

    try:
        user = User.objects.get(username=request.user.username)
        
    except User.DoesNotExist:
        return redirect('rango:index')
    
    userprofile = UserProfile.objects.get_or_create(user=user)[0]

    form = UserProfileForm()
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            
            return redirect('rango:index')
        else:
            print(form.errors)

    context_dict = {'form':form}

    return render(request, 'rango/register_profile.html', context_dict)

@login_required
def profile(request, username):
    print('PROFILE')
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return redirect('rango:index')
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
    {'website': userprofile.website, 'picture': userprofile.picture})
    if request.method == 'POST':
        print("POST REQUEST SUBMITTED")
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)
    return render(request, 'rango/profile.html',
    {'userprofile': userprofile, 'selecteduser': user, 'form': form})

@login_required
def list_profiles(request):
    userprofile_list = UserProfile.objects.all()
    return render(request, 'rango/list_profiles.html',{'userprofile_list' : userprofile_list})

@login_required
def like_category(request):     #this view is actually never shown, it is triggered by AJAX on the backend to deal with likes
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)


#SERVER SIDE COOKIE METHOD

#CLIENT SIDE COOKIES
# def get_server_side_cookie(request, cookie, default_val=None):
#     val = request.session.get(cookie)
#     if not val:
#         val = default_val
#     return val
        
# def visitor_cookie_handler(request, response):
#     # Get the number of visits to the site.
#     # We use the COOKIES.get() function to obtain the visits cookie.
#     # If the cookie exists, the value returned is casted to an integer.
#     # If the cookie doesn't exist, then the default value of 1 is used.
#     visits = int(request.COOKIES.get('visits', '1'))
#     last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
#     last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
#         # If it's been more than a day since the last visit...
#     if (datetime.now() - last_visit_time).seconds > 0:
#         visits = visits + 1
#         # Update the last visit cookie now that we have updated the count
#         response.set_cookie('last_visit', str(datetime.now()))
#     else:
#         # Set the last visit cookie
#         response.set_cookie('last_visit', last_visit_cookie)
#     # Update/set the visits cookie
#     response.set_cookie('visits', visits)

# def index(request):
#     category_list = Category.objects.order_by('-likes')[:5]
#     page_list = Page.objects.order_by('-likes')[:5]
#     visits = int(request.COOKIES.get('visits', '1'))
#     context_dict = {'boldmessage':'TIME TO GO HOME','categories':category_list,'pages':page_list, 'visits':visits}
#     response = render(request, 'rango/index.html', context_dict)
#     visitor_cookie_handler(request, response) #response contains the cookie information
#     return response
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import *


# Create your views here.
def showResults(request):
    if request.method == 'POST':
        kw = request.POST.get('kw')
        sortBy = request.POST.get('sortBy')
        cat = request.POST.get('cat')
        print ("----------------------------------")
        print (sortBy)
        print (cat)
        print ("----------------------------------")
        obj = matchAndSort(keyword=kw,filter=cat,sortBy=sortBy)
        print (obj)
        return render(request, 'search_migrate.html',{'photos': obj, 'category': Category.objects.all()})
    else:
        print ( Photo.objects.all() )
        return render(request, 'search_migrate.html',{'photos': Photo.objects.all(), 'category': Category.objects.all()})

def usr_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print (username, password)
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            return redirect('home')
            #return render(request'search/')
            #return HttpResponse("OK")
        else:
            return HttpResponse("Invalid username and password")
    else:
        return render(request, 'login_migrate.html',{})

def homePage(request):
    return render(request, 'index.html',{"photos": Photo.objects.all(), "sliderP": Photo.objects.all()[::-1][:3] })

@csrf_exempt
@login_required
def create_photo(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            usr = request.user.member
            if usr.exceed_daily_quota():
                return HttpResponse("ERROR! Exceeded daily upload quota! Please upload tomorrow <br><br><a href='/home'>Back to home page</a>")
            if usr.exceed_total_quota():
                return HttpResponse("ERROR! Exceeded total upload quota! Please delete some photo <br><br><a href='/home'>Back to home page</a>")
            tagList = request.POST['tag_info'].split()
            MAX_TAG_NUMBER=10
            if len(tagList) > MAX_TAG_NUMBER:
                return HttpResponse("ERROR! Exceeded maximum number of tags! <br> Please make sure you have less then " + str(MAX_TAG_NUMBER) +" tags <br><br><a href='javascript:history.back()'>Go Back</a>")
            MAX_TAG_LENGTH=10
            for tag in tagList:
                if len(tag) > MAX_TAG_LENGTH:
                    return HttpResponse("ERROR! A tag has exceeded the maximum tag length! <br> Please make sure tags have less than "+ str(MAX_TAG_LENGTH) + " characters <br><br><a href='javascript:history.back()'>Go Back</a>")
            #if request.POST['pic'] == '':
            #    return HttpResponse("ERROR! No Photo selected! Please upload a photo<br><a href='javascript:history.back()'>Go Back</a>")
            new_photo = Photo(title=request.POST['title'], description=request.POST['description'])
            new_photo.imageFile=request.FILES['pic']
            new_photo.save()
            new_photo.associate_tag(request.POST['tag_info'])
            tmp_category = Category.objects.get(name=request.POST['category'])
            tmp_category.photo_set.add(new_photo)
            request.user.member.photo_set.add(new_photo)
            usr.increment_counts()
        #return render(request, 'upload.html',{})
    return HttpResponse("Upload Success!<br><a href='javascript:history.back()'>Go Back</a>")

@csrf_exempt
@login_required
def upload(request):
	return render(request, 'upload.html',{"category":Category.objects.all()})

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import DocumentForm
from .models import Document
from django.contrib.auth.models import User

def signupView(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    pwd = request.POST.get("pwd")

    if request.method == "POST":
        userM= User.objects.create_user(username,email,pwd)
        userM.save()
        return HttpResponseRedirect(reverse('signin'))
    return render(request,"upload/signup.html", {})


# Create your views here.
def loginView(request):
    print("*************Entered Login view *****************")
    if request.method == "POST":
        username = request.POST.get("username")
        PassW = request.POST.get("pass")
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        print(username, PassW)
        # if(re.search(regex,username)):
        #     print("&&&&&&&&&&&&& It is email address &&&&&&&&&&&&&&")
        #     user_email=User.objects.get(email=username)
        #     user = authenticate(username = user_email.username, password=PassW)
        # else:
        #     user = authenticate(username = username, password=PassW)
        user = authenticate(username = username, password=PassW)
        print(user)
        # userV = Profile.objects.filter(user=user)
        # print(userV)
        if user is not None:
            if user.is_active:
                login(request,user)
                request.user.activated=True
                request.user.save()
                # request.userV.active = True
                # request.userV.save()

                # print("is it a Admin :", user.is_itstaff)
                # if user.is_itstaff:
                #     return HttpResponseRedirect(reverse('veri_index'))
                # else:
                context_dict={
                    # 'Role':user.role,
                    'is_active':user.is_authenticated,
                }
                # print("The role of user:",user.role)
                return HttpResponseRedirect(reverse_lazy('form_one'))
                # return reverse_lazy('dashboard', context_dict)
            else:
                return HttpResponse("Account Not Active")
        else:
            print("Someone tried to login and failed")
            print("Mobile_no: {} and password {}".format(username,PassW))
            return HttpResponse("invalid login details supplied!")
    else:
            print("********* Entered render **************")
            return render(request,"upload/index.html", {})



# def model_form_upload(request):
#     print("*************Entered model_form_upload *****************")
#     form = DocumentForm()
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponse("<h1>Success</h1>")
#     return render(request, 'upload/simple_upload.html', {
#         'form': form
#     })

@login_required
def form_upload_view(request):
    form = DocumentForm()
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("<h1>Success</h1> <!DOCTYPE html><html><body style='background-color:powderblue;'></body></html><p>-YOUR FILE HAS BEEN SUCCESFULLY UPLOADED </p><button type='button'>EXECUTE</button> ")

    return render(request, "upload/upload_file.html", {'form': form})

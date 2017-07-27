from django.shortcuts import render
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .models import ipadd_path
from .script import fun

# Create your views here.


@login_required
def index(requests):
    return render_to_response('index.html')


#@login_required
@csrf_exempt
def develop(requests):
    if requests.method == 'GET':
        return render_to_response('develop.html')
    else:
        domain = requests.POST['domain']
        p = ipadd_path.objects.filter(Domain__icontains=domain)
        return render_to_response('develop.html', locals())


@login_required
@csrf_exempt
def ccshopissue(requests, id):
    if requests.method == 'GET':
        id = id
        return render_to_response('ccshop.html', locals())
    else:
        reset = requests.POST['reset']
        ip_path = ipadd_path.objects.get(id=id)
        fun(ip_path.Ipadd, ip_path.Ccshoppath, reset)
        return HttpResponseRedirect('/ccshop/%s' %id)


@login_required
@csrf_exempt
def templates(requests, id):
    if requests.method == 'GET':
        id = id
        return render_to_response('templates.html', locals())
    else:
        reset = requests.POST['reset']
        ip_path = ipadd_path.objects.get(id=id)
        fun(ip_path.Ipadd, ip_path.Themespath, reset)
        return HttpResponseRedirect('/templates/%s' % id)


@csrf_exempt
def login_site(requests):
    if requests.method == 'POST':
        username = requests.POST.get('username')
        password = requests.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(requests, user)
            return HttpResponseRedirect('/develop/')
        else:
            return render_to_response('login.html',{'login_err': 'Please recheck your username or password!'})
    return render_to_response('login.html')


@login_required
def logout_site(requests):
    logout(requests)
    return render_to_response('login.html')
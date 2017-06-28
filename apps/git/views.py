from django.shortcuts import render
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout


from .models import ipadd_path
from .script import fun

# Create your views here.
@csrf_exempt
def develop(requests):
    if requests.method == 'GET':
        return render_to_response('develop.html')
    else:
        domain = requests.POST['domain']
        p = ipadd_path.objects.filter(domain__icontains=domain).exclude(devipadd__isnull=True)
        return render_to_response('develop.html', locals())


@csrf_exempt
def developissue(requests, id):
    if requests.method == 'GET':
        id = id
        return render_to_response('developissue.html', locals())
    else:
        reset = requests.POST['reset']
        ip_path = ipadd_path.objects.get(id=id)
        print ip_path.devipadd, ip_path.devpath, reset
        fun(ip_path.devipadd, ip_path.devpath, reset)
        return HttpResponseRedirect('/developissue/%s' %id)


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


def logout_site(requests):
    logout(requests)
    return render_to_response('login.html')
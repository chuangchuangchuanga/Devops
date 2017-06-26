from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt


from .models import ipadd_path


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
        return render_to_response('developissue.html')

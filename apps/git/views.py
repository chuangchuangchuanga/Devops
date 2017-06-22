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
        p = ipadd_path.objects.get(domain__icontains=domain)
        return render_to_response('develop.html', locals())


def developissue(requests):
    if requests.method == 'GET':
        return render_to_response('developissue.html')
    else:
        pass